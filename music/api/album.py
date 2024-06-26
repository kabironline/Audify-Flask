from flask_restful import Resource, request
from flask_jwt_extended import get_jwt_identity, jwt_required, current_user
import music.services as music_services
import membership.services as membership_services
from datetime import datetime
from core.db import get_redis
import json

class AlbumAPI(Resource):
  @jwt_required(optional=True)
  def get(self, album_id):
    r = get_redis()
    album_dict = None
    album = None
    if r.get(f"album:{album_id}") is not None:
      album_dict = json.loads(r.get(f"album:{album_id}"))
    else:
      album = music_services.get_album_by_id(album_id)
      album_dict = music_services.get_album_dict(album) if album is not None else None
    
    if album is None and album_dict is None:
      return {"error": "Album not found"}, 404
    
    album_items = music_services.get_album_tracks_by_album_id(album_id)
    ratings = {}    
    
    r.set(f"album:{album_id}", json.dumps(album_dict), ex=3600)
    auth_header = request.headers.get("Authorization")
    if auth_header != '':
      user_id = get_jwt_identity()
      user = membership_services.get_user_by_id(user_id)
      ratings = music_services.get_track_rating_for_user(user.id, *[album_item.id for album_item in album_items])
    for track in album_items:
      track.rating = ratings.get(track.id, None)
    tracks = [music_services.get_track_dict(album_item) for album_item in album_items]
    album_dict["tracks"] = tracks
    return {
      "album": album_dict
    }, 200
  
  @jwt_required()
  def post(self):
    request_data = request.form
    album_name = request_data.get("album_name")
    album_description = request_data.get("album_description")
    album_art = request.files.get("album_art")
    release_date = request_data.get("release_date")
    creator = current_user.channel
    
    release_date = datetime.strptime(release_date, "%Y-%m-%d")

    album = music_services.create_album(
      name=album_name,
      description=album_description,
      release_date=release_date,
      album_art=album_art,
      channel_id=creator.id,
    )
    count = 0
    if "album_tracks" in request_data:
      album_tracks = request_data.get("album_tracks")
      if type(album_tracks) == str: album_tracks = [album_tracks]
      if len(album_tracks) > 0:
        for track_id in album_tracks:
          if track_id == "": continue
          track_id = int(track_id)
          count += 1
          music_services.create_album_item(
            album_id=album.id,
            track_id=track_id,
            user_id=creator.id,
          )
      if len(album_tracks) == 0 or count == 0:
        music_services.delete_album(album.id, creator.id, True)
        return {"error": "No tracks found"}, 400

    r = get_redis()
    
    if r.get(f"latest-albums-5"):
      r.delete(f"latest-albums-5")

    album_dict = music_services.get_album_dict(album)

    return {"action": "created", "album":album_dict}, 201
  
  @jwt_required()
  def put(self, album_id):
    request_data = request.form
    album_name = request_data.get("album_name")
    album_tracks = request_data.get("album_tracks")
    release_date = request_data.get("release_date")
    
    release_date = datetime.strptime(release_date, "%Y-%m-%d")
    
    album_art = request.files.get("album_art") if "album_art" in request.files else None

    album = music_services.get_album_by_id(album_id)
    if album is None:
      return {"error": "Album not found"}, 404
    
    if album.channel.id != current_user.channel.id:
      return {"error": "Unauthorized"}, 401

    album = music_services.update_album(
      album_id=album_id,
      name=album_name,
      release_date=release_date,
      album_art=album_art,
    )

    r = get_redis()
    r.delete(f"album:{album_id}")
    r.set(f"album:{album_id}", json.dumps(music_services.get_album_dict(album)), ex=3600)

    # deleting all album items and adding new ones
    album_items = music_services.get_album_items_by_album_id(album_id)
    for album_item in album_items:
      music_services.delete_album_item(album_item.id)


    if album_tracks is not None:
      if type(album_tracks) == str: album_tracks = album_tracks.split(",")
      for track_id in album_tracks:
        track_id = int(track_id)
        music_services.create_album_item(
          album_id=album.id,
          track_id=track_id,
          user_id=current_user.channel.id,
        )

    return {"action": "updated"}, 200
  
  @jwt_required()
  def delete(self, album_id):
    album = music_services.get_album_by_id(album_id)
    
    if album is None:
      return {"error": "Album not found"}, 404
    

    album_items = music_services.get_album_items_by_album_id(album_id)

    if album.created_by != current_user.channel.id:
      return {"error": "Unauthorized"}, 401

    for album_item in album_items:
      music_services.delete_album_item(album_item.id)

    music_services.delete_album(album_id, current_user.channel.id, True)

    r = get_redis()
    r.delete(f"album:{album_id}")

    r = get_redis()
    if r.get(f"latest-albums-5"):
      latest_albums = json.loads(r.get(f"latest-albums-5"))["albums"]
      for i, album in enumerate(latest_albums):
        if album["id"] == album_id:
          r.delete(f"latest-albums-5")
          break
    return {"action": "deleted"}, 200


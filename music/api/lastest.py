from flask_restful import Resource, request
from music.services import get_latest_tracks, get_track_dict, get_latest_albums, get_album_dict, get_latest_playlist,get_playlist_dict, get_track_rating_for_user
from core.db import get_redis
import json

class LatestAPI(Resource):
  def get(self):
    latest_json = {}
    
    count = request.args.get("n", 5)
    route = request.path.split("/")[3]
    
    r = get_redis()
    r_latest = r.get(f'latest-{route}-{count}')
    r_latest_counter= int(r.get(f'latest-{route}-{count}-counter') or 0) 
    if r_latest and r_latest_counter:
      if r_latest_counter == 1:
        r.expire(f'latest-{route}-{count}-counter', 1)
        r.expire(f'latest-{route}-{count}', 1)
      r.set(f'latest-{route}-{count}-counter', r_latest_counter - 1)
      return json.loads(r_latest), 200
    
    if route == "albums":
      latest = get_latest_albums(count)
      latest_json = [(get_album_dict(album)) for album in latest]
    elif route == "tracks":
      latest = get_latest_tracks(count)
      
      latest_json = [(get_track_dict(track)) for track in latest]
    
    elif route == "playlists":
      latest = get_latest_playlist(count)
      latest_json = [(get_playlist_dict(playlist)) for playlist in latest]
    else:
      return {
        "error": "Invalid route"
      }, 400
    final_json = {
      "latest": latest_json,
    } 
    r.set(f'latest-{route}-{count}', json.dumps(final_json))
    r.set(f'latest-{route}-{count}-counter', 10)
    return final_json, 200
from flask_restful import Resource, request
from music.services import get_latest_tracks, get_track_dict, get_latest_albums, get_album_dict

class LatestAPI(Resource):
  def get(self):
    # Check the route if it has "tracks" or "albums"

    route = request.path.split("/")[3]

    if route == "albums":
      latest = get_latest_albums()
      latest_json = [(get_album_dict(album)) for album in latest]
      return {
        "latest": latest_json,
      }, 200
    elif route == "tracks":
      latest = get_latest_tracks()
      latest_json = [(get_track_dict(track)) for track in latest]
      
      return {
        "latest": latest_json,
      }, 200
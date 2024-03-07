from flask_restful import Resource, request
from music.services import get_top_tracks,get_top_rated_tracks, get_track_dict, get_top_rated_channels, get_channel_dict, get_track_rating_for_user
from flask_jwt_extended import jwt_required, current_user

class TopAPI(Resource):
  @jwt_required(optional=True)
  def get(self):
    # Check the route if it has "tracks" or "channels"
    # check how many number of tracks or channels to return
    route = request.path.split("/")[3]
    count = request.args.get("n", 10)
    if route == "tracks":
      tracks = []
      mode = request.path.split("/")[5]
      if mode == "ratings":
        tracks = get_top_rated_tracks(count)
      elif mode == "views":
        tracks = get_top_tracks(count)
      if request.headers.get("Authorization"):
        ratings = get_track_rating_for_user(current_user.id, *[track.id for track in tracks])
        for track in tracks:
          track.rating = ratings.get(track.id, None)
      track_json = [(get_track_dict(track)) for track in tracks]
      return {
        "top": track_json,
      }, 200
    elif route == "channels":
      top = get_top_rated_channels(count)
      top_json = [(get_channel_dict(channel)) for channel in top]
      return {
        "top": top_json,
      }, 200
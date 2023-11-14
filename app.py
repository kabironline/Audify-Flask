from flask import Flask, redirect, url_for, request, Response, session
from flask_migrate import Migrate
from flask_restful import Api
from flask_cors import CORS
import os
import core

from commands.db import *
from core.db import db
from core import api
import membership.routes
import music.routes
import music.api


app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})

current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_dir, "core/db/db.sqlite3")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_path
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

db.init_app(app)
migrate = Migrate(app, db)

api = Api(app)
api.add_resource(
    music.api.RatingAPI,
    "/api/rating/<int:track_id>",
)
api.add_resource(
    music.api.CommentAPI,
    "/api/rating/<int:track_id>",
)

core.set_api(api)


@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        res = Response()
        res.headers["X-Content-Type-Options"] = "*"
        return res


app.cli.add_command(create_tables)
app.cli.add_command(drop_table)
app.cli.add_command(drop_all_tables)
app.cli.add_command(create_superuser)


@app.route("/")
def entry():
    if core.get_current_user() is None:
        return redirect(url_for("login"))
    return redirect(url_for("home"))


app.add_url_rule("/home", "home", music.routes.home)
app.add_url_rule("/login", "login", membership.routes.login, methods=["GET", "POST"])
app.add_url_rule(
    "/register", "register", membership.routes.register, methods=["GET", "POST"]
)
app.add_url_rule("/upload", "upload", music.routes.upload, methods=["GET", "POST"])
app.add_url_rule("/playlist", "playlist", music.routes.playlist)

# Players and Tracks
app.add_url_rule("/player/<int:track_id>", "player", music.routes.player)
app.add_url_rule("/tracks/<int:track_id>", "track", music.routes.track)
app.add_url_rule(
    "/tracks/<int:track_id>/cover", "track_cover", music.routes.track_cover
)
app.add_url_rule(
    "/tracks/<int:track_id>/media", "track_media", music.routes.track_media
)

# Comments
app.add_url_rule(
    "/tracks/<int:track_id>/comments",
    "create_comment",
    music.routes.post_comment_route,
    methods=["POST"],
)
app.add_url_rule(
    "/tracks/<int:track_id>/comments/<int:comment_id>/delete",
    "delete_comment",
    music.routes.delete_comment_route,
    # methods=["POST"],
)


app.add_url_rule("/player_controls", "player_controls", music.routes.player_controls)
app.add_url_rule("/explore", "explore", music.routes.explore)
app.add_url_rule("/new_releases", "new_releases", music.routes.new_releases)
app.add_url_rule(
    "/new_releases/albums", "new_releases_albums", music.routes.new_releases_albums
)
app.add_url_rule(
    "/new_releases/tracks", "new_releases_tracks", music.routes.new_releases_tracks
)
app.add_url_rule("/top_charts", "top_charts", music.routes.top_charts)
app.add_url_rule("/dashboard", "dashboard", membership.routes.dashboard)
app.add_url_rule("/dashboard/<int:user_id>", "dashboard", membership.routes.dashboard)

# Register the media directory as a static directory

app.add_url_rule(
    "/media/<path:filename>",
    "media",
    build_only=True,
    subdomain="static",
)

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        debug=True,
    )

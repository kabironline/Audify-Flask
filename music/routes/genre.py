from flask import render_template, redirect, url_for, request
import music.services
import membership.services
import core


def genre_tracks(genre_id):
    if core.get_current_user() is None:
        return redirect(url_for("login"))

    q = request.args.get("q")

    genre = music.services.get_genre_by_id(genre_id)
    tracks = music.services.get_genre_tracks(genre_id)

    return render_template(
        "music/all_tracks.html", title=genre.name, all_tracks=tracks, q=q
    )

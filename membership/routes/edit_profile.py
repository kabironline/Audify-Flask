from flask import render_template, request, redirect, url_for
import core
from membership.services import (
    update_user,
    get_user_channels,
    get_channel_dict,
    get_channel_by_id,
)
from music.services import get_playlist_by_user, get_playlist_dict


def edit_profile():
    user = core.get_current_user()
    if user is None:
        return redirect(url_for("login"))

    if request.method == "POST":
        request_data = request.form
        if request_data.get("password") != user.password:
            return render_template(
                "membership/edit_profile.html",
                current_user=user,
                error="Incorrect Old Password Password",
            )

        user.username = request_data.get("username")
        user.nickname = request_data.get("nickname")
        user.bio = request_data.get("bio")

        if request_data.get("new_password") != "":
            user.password = request_data.get("new_password")

        request_data = request.files
        user.avatar = None
        if request_data.get("avatar"):
            user.avatar = request_data.get("avatar")

        update_user(user)
        # Checking if user is a part of any channel
        members = get_user_channels(user.id)
        channel = None
        if len(members) != 0:
            channel = []
            for member in members:
                channel.append(get_channel_dict(get_channel_by_id(member.channel_id)))

        playlist = []
        playlist_search = get_playlist_by_user(user.id)
        for playlist_item in playlist_search:
            playlist.append(get_playlist_dict(playlist_item))

        core.set_current_user(user, channel, playlist)
        return redirect(url_for("edit_profile"))

    return render_template("membership/edit_profile.html", current_user=user)
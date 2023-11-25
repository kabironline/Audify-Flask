from flask import render_template, request, redirect, url_for
from membership.services import get_user_by_id, get_channel_by_id, get_channel_members
import music.services
from admin.services import get_whitelist_by_channel_id
import core


def dashboard(user_id=None):
    user = core.get_current_user()
    if user is None:
        return redirect(url_for("login"))

    user_id = user.id if user_id is None else user_id
    user = get_user_by_id(user_id) if user_id is not user.id else user

    recent_tracks = music.services.get_recent_by_user_id(user_id)
    ratings = music.services.get_track_rating_for_user(
        user_id, *[t.id for t in recent_tracks]
    )

    for track in recent_tracks:
        track.rating = ratings[track.id] if track.id in ratings else None

    playlists = music.services.get_playlist_by_user(user_id)

    return render_template(
        "membership/dashboard.html",
        user=user,
        own_profile=False,
        recent_tracks=recent_tracks,
        playlists=playlists,
    )


def dashboard_channel(channel_id=None):
    channel = get_channel_by_id(channel_id)
    user = core.get_current_user()

    if user is None:
        return redirect(url_for("login"))

    # Check if the user is a member of the channel
    is_member = any(
        [member.user_id == user.id for member in get_channel_members(channel_id)]
    )

    if channel.blacklisted:
        return redirect(url_for("home"))

    if channel is None:
        # TODO: Redirect to 404 page
        return redirect(url_for("home"))

    channel_tracks = music.services.get_tracks_by_channel(channel_id)
    for track in channel_tracks:
        track.channel = channel

    albums = music.services.get_album_by_user(channel_id)
    for album in albums:
        album.channel = channel

    channel.whitelist = get_whitelist_by_channel_id(channel_id)

    return render_template(
        "membership/dashboard_channel.html",
        channel=channel,
        own_profile=is_member,
        channel_tracks=channel_tracks,
    )


def dashboard_channel_tracks(channel_id=None):
    channel = get_channel_by_id(channel_id)

    if channel is None:
        # TODO: Redirect to 404 page
        return redirect(url_for("home"))

    channel_tracks = music.services.get_tracks_by_channel(channel_id)
    for track in channel_tracks:
        track.channel = channel

    return render_template(
        "music/all_tracks.html", all_tracks=channel_tracks, title=channel.name
    )

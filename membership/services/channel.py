import os
from core.db import get_session, get_test_session
from core import get_current_user
import membership.models.channel as channel_model
import membership.services as services
from werkzeug.datastructures import FileStorage
import datetime


def create_channel(name, description, api=False):
    """
    Creates a new channel with the given name and description.

    If there is already a channel with the given name, it raises an exception.
    """
    session = get_session()
    if session.query(channel_model.Channel).filter_by(name=name).first() is not None:
        return {"error": "Channel already exists"}, 400

    user = None
    try:
        user = get_current_user()
    except Exception as e:
        pass
    if user is None:
        if api:
            user = services.get_user_by_username(username="api_superuser")
        else:
            raise Exception("User not found")

    new_channel = channel_model.Channel(
        name=name,
        description=description,
        created_by=user.id,
        last_modified_by=user.id,
        created_at=datetime.datetime.now(),
        last_modified_at=datetime.datetime.now(),
    )
    session.add(new_channel)
    session.commit()

    return new_channel


def get_channel_by_id(channel_id) -> channel_model.Channel:
    """
    Returns the channel with the given id.

    If there is no channel with the given id, it returns None.
    """
    session = get_session()
    return session.query(channel_model.Channel).filter_by(id=channel_id).first()


def get_channel_by_name(name) -> channel_model.Channel:
    """
    Returns the channel with the given name.

    If there is no channel with the given name, it returns None.
    """
    session = get_session()

    search = search_channels(name)

    return search[0] if len(search) > 0 else None


def get_all_channels() -> [channel_model.Channel]:
    """
    Returns all the channels.
    """
    session = get_session()
    return session.query(channel_model.Channel).all()


def update_channel(
    channel_id, name, description, channel_art: FileStorage = None
) -> channel_model.Channel:
    """
    Updates the channel with the given id.

    If there is no channel with the given id, it raises an exception.
    """
    session = get_session()
    channel = session.query(channel_model.Channel).filter_by(id=channel_id).first()
    if channel is None:
        raise Exception("Channel not found")

    channel.name = name if name is not None else channel.name
    channel.description = description if description is not None else channel.description
    channel.last_modified_at = datetime.datetime.now()
    session.commit()

    try:
        os.mkdir(f"media/channels/{channel_id}")
    except FileExistsError:
        pass

    if channel_art:
        channel_art.save(f"media/channels/{channel_id}/avatar.png")

    return channel


def delete_channel_by_id(channel_id):
    """
    Deletes the channel with the given id.

    If there is no channel with the given id, it raises an exception.
    """
    session = get_session()
    channel = session.query(channel_model.Channel).filter_by(id=channel_id).first()
    if channel is None:
        raise Exception("Channel not found")

    session.delete(channel)
    session.commit()


def get_channel_dict(channel: channel_model.Channel):
    return {
        "id": channel.id,
        "name": channel.name,
        "description": channel.description,
        "created_by": channel.created_by,
        "last_modified_by": channel.last_modified_by,
        "created_at": channel.created_at,
        "last_modified_at": channel.last_modified_at,
    }


def search_channels(q):
    search = channel_model.ChannelSearch.query.filter(
        channel_model.ChannelSearch.name.match(f"{q}")
    )

    result = []
    for channel in search:
        result.append(get_channel_by_id(channel.rowid))

    return result
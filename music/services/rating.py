from music.models import Rating
from core.db import get_session
from datetime import datetime
from sqlalchemy import tuple_, func


def like_track(track_id, user_id):
    create_or_update_rating(track_id, user_id, 1)


def dislike_track(track_id, user_id):
    create_or_update_rating(track_id, user_id, -1)


def create_or_update_rating(track_id, user_id, rating):
    """
    This funcation updates the rating of a track by a user. If the user has already rated the track and it is the same rating,
    then it deletes the rating.

    If the user has not rated the track, then it creates a new rating.

    Otherwise, it updates the existing rating.

    """
    session = get_session()
    user_rating = get_rating_by_user_and_track_id(user_id, track_id)
    if user_rating == None:
        # create a new rating
        new_rating = Rating(
            rating=rating,
            track_id=track_id,
            user_id=user_id,
            created_by=user_id,
            last_modified_by=user_id,
            last_modified_at=datetime.now(),
            created_at=datetime.now(),
        )
        session.add(new_rating)
        session.commit()

        return new_rating
    else:
        # update the existing rating

        if user_rating.rating == rating:
            # delete the rating
            session.delete(user_rating)
            session.commit()
            return None

        user_rating.rating = rating
        user_rating.last_modified_by = user_id
        user_rating.last_modified_at = datetime.now()
        session.commit()

        return user_rating


def get_track_rating(track_id):
    """
    This function returns the average rating of a track.
    """
    session = get_session()

    ratings = session.query(Rating).filter(Rating.track_id == track_id).all()

    if not ratings:
        average_rating = None
    else:
        average_rating = session.query(func.avg(Rating.rating)).filter(Rating.track_id == track_id).scalar()

    return average_rating


def get_rating_by_user_and_track_id(user_id, track_id):
    """
    This function returns the rating of a track by a user.
    """
    session = get_session()

    rating = (
        session.query(Rating)
        .filter(Rating.track_id == track_id)
        .filter(Rating.user_id == user_id)
        .first()
    )

    return rating


def get_track_rating_for_user(user_id, *track_ids):
    """
    This function returns the rating of a track by a user.

    It returns a dictionary of track_id and rating.
    """
    session = get_session()

    ratings = (
        session.query(Rating)
        .filter(Rating.track_id.in_(track_ids))
        .filter(Rating.user_id == user_id)
        .all()
    )

    ratings = {rating.track_id: rating.rating for rating in ratings}

    return ratings


def clear_track_rating(track_id):
    """
    This function clears all the ratings of a track.
    """
    session = get_session()

    ratings = session.query(Rating).filter(Rating.track_id == track_id).all()

    for rating in ratings:
        session.delete(rating)

    session.commit()


def delete_rating(track_id, user_id):
    session = get_session()

    rating = (
        session.query(Rating)
        .filter(Rating.track_id == track_id)
        .filter(Rating.user_id == user_id)
        .first()
    )

    session.delete(rating)

    session.commit()


def delete_track_ratings(track_id):
    session = get_session()

    ratings = session.query(Rating).filter(Rating.track_id == track_id).all()

    for rating in ratings:
        session.delete(rating)

    session.commit()

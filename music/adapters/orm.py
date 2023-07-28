from sqlalchemy import Table, MetaData, Column, Integer, String, Date, DateTime, ForeignKey
from sqlalchemy.orm import mapper, relationship, synonym

from music.domainmodel.album import Album
from music.domainmodel.artist import Artist
from music.domainmodel.genre import Genre
from music.domainmodel.review import Review
from music.domainmodel.track import Track
from music.domainmodel.user import User

metadata = MetaData()

albums_table = Table(
    'albums', metadata,
    Column('album_id', Integer, primary_key=True, autoincrement=True),
    Column('title', String(255)),
    Column('album_url', String(255)),
    Column('album_type', String(255)),
    Column('release_year', String(255)),
)

artists_table = Table(
    'artists', metadata,
    Column('artist_id', Integer, primary_key=True, autoincrement=True),
    Column('full_name', String(255))
)

genres_table = Table(
    'genres', metadata,
    Column('genre_id', Integer, primary_key=True, autoincrement=True),
    Column('genre_name', String(255))
)

reviews_table = Table(
    'reviews', metadata,
    Column('review_text', String(1024)),
    Column('rating', Integer, nullable=False),
    Column('timestamp', Date, nullable=False),
    Column('author_name', String(64), primary_key=True),
    Column('track_id', ForeignKey('tracks.track_id'), primary_key=True)
)

tracks_table = Table(
    'tracks', metadata,
    Column('track_id', Integer, primary_key=True, autoincrement=True),
    Column('title', String(255)),
    Column('track_url', String(255)),
    Column('track_duration', Integer),
    Column('image_file', String(255)),
    Column('track_file', String(255)),
    Column('album_id', ForeignKey('albums.album_id')),
    Column('artist_id', ForeignKey('artists.artist_id'))
)

track_genres_table = Table(
    'track_genres', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('track_id', ForeignKey('tracks.track_id')),
    Column('genre_id', ForeignKey('genres.genre_id'))
)

users_table = Table(
    'users', metadata,
    Column('user_id', Integer, primary_key=True, autoincrement=True),
    Column('user_name', String(255)),
    Column('password', String(255)),
)

def map_model_to_tables():
    mapper(Album, albums_table, properties={
        '_Album__album_id': albums_table.c.album_id,
        '_Album__title': albums_table.c.title,
        '_Album__album_url': albums_table.c.album_url,
        '_Album__album_type': albums_table.c.album_type,
        '_Album__release_year': albums_table.c.release_year,
    })

    mapper(Artist, artists_table, properties={
        '_Artist__artist_id': artists_table.c.artist_id,
        '_Artist__full_name': artists_table.c.full_name,
    })

    mapper(Genre, genres_table, properties={
        '_Genre__genre_id': genres_table.c.genre_id,
        '_Genre__name': genres_table.c.genre_name
    })

    mapper(Review, reviews_table, properties={
        '_Review__review_text': reviews_table.c.review_text,
        '_Review__rating': reviews_table.c.rating,
        '_Review__timestamp': reviews_table.c.timestamp,
        '_Review__author_name': reviews_table.c.author_name,
        '_Review__track_id': reviews_table.c.track_id,
    })

    mapper(Track, tracks_table, properties={
        '_Track__track_id': tracks_table.c.track_id,
        '_Track__title': tracks_table.c.title,
        '_Track__track_url': tracks_table.c.track_url,
        '_Track__track_duration': tracks_table.c.track_duration,
        '_Track__image_file': tracks_table.c.image_file,
        '_Track__track_file': tracks_table.c.track_file,
    })

    mapper(User, users_table, properties={
        '_User__user_id': users_table.c.user_id,
        '_User__user_name': users_table.c.user_name,
        '_User__password': users_table.c.password,
    })
import pytest

import music.adapters.repository as repo
from music.adapters.database_repository import SqlAlchemyRepository
from music.domainmodel.user import User, Track

def test_repository_can_add_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user = User('epicgamer', '1234567890')
    repo.add_user(user)
    repo.add_user(User('amongus', '1987654321'))

    assert session_factory.get_user('dbowie') is user and session_factory.get_user('amongus') is not None

def test_repository_can_retrieve_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user = repo.get_user('fmercury')

    assert user == User('fmercury', '1234567890')

def test_repository_does_not_retrieve_a_non_existent_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user = repo.get_user('theImpasta')

    assert user is None

def test_repository_can_add_song(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    song = Track('screw the nether', 2016)
    repo.get_track(song)

    assert repo.get_song(1) == song

def test_repository_can_retrieve_song(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    song = repo.get_track(1)
    assert song.track_id == 1

def test_repository_does_not_retrieve_a_non_existent_song(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    song = repo.get_track(999999999999999)
    assert song is None

def test_repository_can_retrieve_artist(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    artist = repo.get_artist(1)
    assert artist.artist_id == 1

def test_repository_does_not_retrieve_a_non_existent_artist(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    artist = repo.get_artist(999999999999999)
    assert artist is None

def test_repository_can_retrieve_genre(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    genre = repo.get_genre(1)
    assert genre.genre_id == 1

def test_repository_does_not_retrieve_a_non_existent_genre(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    genre = repo.get_genre(999999999999999)
    assert genre is None

def test_repository_can_sort_by_title(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    songs = repo.get_tracks_by_title()
    assert songs[0].title < songs[40].title

def test_repository_can_sort_by_artist(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    songs = repo.get_tracks_by_artist()
    assert songs[0].artist < songs[40].artist

def test_repository_can_sort_by_album(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    songs = repo.get_tracks_by_album()
    assert songs[0].album < songs[40].album

def test_repository_can_sort_by_duration(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    songs = repo.get_tracks_by_duration()
    assert songs[0].duration < songs[40].duration
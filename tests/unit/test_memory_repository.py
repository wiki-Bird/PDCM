from music.domainmodel.user import User
from music.domainmodel.track import Track
from music.domainmodel.review import Review

def test_repository_can_add_a_user(in_memory_repo):
    user = User(123456789, 'liam', 'password123')
    in_memory_repo.add_user(user)

    # this coincidentally also tests retrieval of a user
    assert in_memory_repo.get_user('liam') is user

def test_repository_does_not_retrieve_a_non_existent_user(in_memory_repo):
    user = in_memory_repo.get_user('any name')
    assert user is None

def test_repository_can_add_track(in_memory_repo):
    track = Track(123, 'Faded')
    in_memory_repo.add_track(track)

    assert in_memory_repo.get_track(123) is track

def test_repository_can_retrieve_track(in_memory_repo):
    track = in_memory_repo.get_track(2)

    assert track.title == 'Food'
    assert track.artist.full_name == 'AWOL'

def test_repository_does_not_retrieve_a_non_existent_article(in_memory_repo):
    track = in_memory_repo.get_track(543210)
    assert track is None

def test_repository_can_add_and_retrieve_a_review(in_memory_repo):
    track = in_memory_repo.get_track(2)
    review = Review(track, 'my review text', 4, 'obama')
    in_memory_repo.add_review(review)

    received_review = in_memory_repo.get_reviews_of_track(track.track_id)
    assert len(received_review) == 1
    assert received_review[0] is review
    
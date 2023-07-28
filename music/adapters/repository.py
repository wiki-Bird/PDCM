import abc
from typing import List

from music.domainmodel.track import Track, Artist, Genre
from music.domainmodel.user import User
from music.domainmodel.review import Review

repo_instance = None

class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def get_tracks_sorted_by_artist(self, reverse=False) -> List[Track]:
        """ Returns a list of Tracks sorted alphabetically by Artist name. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_tracks_sorted_by_album(self, reverse=False) -> List[Track]:
        """ Returns a list of Tracks sorted alphabetically by Album name. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_tracks_sorted_by_id(self, reverse=False) -> List[Track]:
        """ Returns a list of Tracks sorted by id. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_tracks_sorted_by_title(self, reverse=False) -> List[Track]:
        """ Returns a list of Tracks sorted alphabetically by Track title. """
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_tracks_sorted_by_duration(self, reverse=False) -> List[Track]:
        """ Returns a list of Tracks sorted by duration. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_track(self, track_id: int) -> Track:
        """ Returns a Track object with the given id. """
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_tracks_by_genre(self, genre_id: int) -> List[Track]:
        """ Returns a list of Tracks that match the genre id. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_tracks_by_genres(self) -> dict:
        """ Returns a dictionary where the key is the genre and the value is a list of Tracks that match the genre id. """
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_genre(self, genre_id: int) -> Genre:
        """ Returns a Genre object with the given id. """
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_tracks_from_artist(self, artist_id: int) -> List[Track]:
        """ Returns a list of Tracks that match the artist id. """
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_artist(self, artist_id: int) -> Artist:
        """ Returns an Artist object with the given id. """
        raise NotImplementedError
    
    @abc.abstractmethod
    def add_track(self, track: Track):
        """ Adds a Track to the repository. """
        raise NotImplementedError
    
    @abc.abstractmethod
    def add_user(self, user: User):
        """ Adds a User to the repository. """
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_user(self, username: str) -> User:
        """ Returns a User object with the given username. """
        raise NotImplementedError


    @abc.abstractmethod
    def get_reviews_of_track(self, track_id: int) -> list[Review]:
        """ Returns a list of Review objects of the given track. """
        raise NotImplementedError

    @abc.abstractmethod
    def add_review(self, review: Review):
        """ Adds a Review object to the repository. """
        raise NotImplementedError

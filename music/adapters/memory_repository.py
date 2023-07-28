import os
from pathlib import Path
from music.adapters.csvdatareader import TrackCSVReader
from music.adapters.repository import AbstractRepository
from music.domainmodel.track import Album, Artist, Genre, Track
from music.domainmodel.playlist import PlayList
from music.domainmodel.review import Review
from music.domainmodel.user import User
from music.track import track

class MemoryRepository(AbstractRepository):
    def __init__(self):
        self.__albums = set[Album]()
        self.__artists = set[Artist]()
        self.__genres = set[Genre]()
        self.__playlists = set()
        self.__reviews = set[Review]()
        self.__tracks = set[Track]()
        self.__users = set[User]()

    def add_album(self, album: Album):
        self.__albums.add(album)

    def add_artist(self, artist: Artist):
        self.__artists.add(artist)
        
    def add_genre(self, genre: Genre):
        self.__genres.add(genre)

    def add_playlist(self, playList: PlayList):
        self.__playlists.add(playList)
    
    def add_review(self, review: Review):
        self.__reviews.add(review)

    def add_track(self, track: Track):
        self.__tracks.add(track)
        
    def add_user(self, user: User):
        self.__users.add(user)
    
    def get_tracks_sorted_by_album(self, reverse=False):
        return sorted(self.__tracks, key = lambda track: '' if track.album is None else track.album.title.lower(), reverse = reverse)

    def get_tracks_sorted_by_artist(self, reverse=False):
        return sorted(self.__tracks, key = lambda track: '' if track.artist is None else track.artist.full_name.lower(), reverse = reverse)

    def get_tracks_sorted_by_id(self, reverse=False):
        return sorted(self.__tracks, key = lambda track: track.track_id, reverse = reverse)

    def get_tracks_sorted_by_title(self, reverse=False):
        return sorted(self.__tracks, key = lambda track: '' if track.title is None else track.title.lower(), reverse = reverse)
    
    def get_tracks_sorted_by_duration(self, reverse=False):
        return sorted(self.__tracks, key = lambda track: track.track_duration, reverse = reverse)
    
    def get_track(self, track_id: int):
        for track in self.__tracks:
            if track.track_id == track_id:
                return track
        return None

    # return a list of track objects that match the genre id
    def get_tracks_by_genre(self, genre_id: int):
        tracks = []
        for track in self.__tracks:
            for genre in track.genres:
                if genre.genre_id == genre_id:
                    tracks.append(track)
        return tracks
    
    # return a dictonary where the key is the genre and the value is a list of tracks that match the genre id
    def get_tracks_by_genres(self):
        tracks = {}
        for track in self.__tracks:
            for genre in track.genres:
                if genre in tracks:
                    tracks[genre].append(track)
                else:
                    tracks[genre] = [track]
        return tracks
    
    # get a genre object by genre id
    def get_genre(self, genre_id: int):
        for genre in self.__genres:
            if genre.genre_id == genre_id:
                return genre
        return None
    
    def get_tracks_from_artist(self, artist_id: int):
        tracks = []
        for track in self.__tracks:
            if track.artist.artist_id == artist_id:
                tracks.append(track)
        return tracks
    
    def get_artist(self, artist_id: int):
        for artist in self.__artists:
            if artist.artist_id == artist_id:
                return artist
        return None

    def get_tracks_from_album(self, album_id: int):
        tracks = []
        for track in self.__tracks:
            if track.album is not None and track.album.album_id == album_id:
                tracks.append(track)
        return tracks
    
    def get_album(self, album_id: int):
        for album in self.__albums:
            if album is not None and album.album_id == album_id:
                return album
        return None
    
    def get_user(self, user_name):
        return next((user for user in self.__users if user.user_name == user_name), None)

    def get_reviews_of_track(self, track_id: int):
        print(f'getting reviews of {track_id}, {len([i for i in self.__reviews if i.track.track_id == track_id])}')
        return [i for i in self.__reviews if i.track.track_id == track_id]

    def add_review(self, review: Review):
        print(f'adding review of {review.track.title} [{review.track.track_id}] (by {review.author_name})')
        self.__reviews.add(review)
    
    def get_recommended_tracks(self, origin_track: int):
        tracks = []
        for track in self.__tracks:
            if track == origin_track or track in tracks:
                pass
            elif track.artist.artist_id == origin_track.artist.artist_id:
                tracks.append(track)
            else:
                for newGenre in origin_track.genres:
                    if newGenre in track.genres:
                        tracks.append(track)
        return tracks
    
    def get_recommended_tracks_for_user(self, user_name: str):
        output = []
        # get all reviews by the user
        reviews = [i for i in self.__reviews if i.author_name == user_name]

        # get all tracks reviewed by the user in a dictionary where the key is the track rating 1-5 and the value is a list of tracks with that rating
        tracks_by_rating = {}
        for review in reviews:
            if review.rating in tracks_by_rating:
                tracks_by_rating[review.rating].append(review.track)
            else:
                tracks_by_rating[review.rating] = [review.track]
        
        # create dictionaries of the artists and genres positively reviewed (3 or more stars) where the key is the artist/genre and the value is the number of times it was reviewed
        artists = {}
        genres = {}
        for rating in tracks_by_rating:
            if rating >= 3:
                for track in tracks_by_rating[rating]:
                    if track.artist in artists:
                        artists[track.artist] += 1
                    else:
                        artists[track.artist] = 1
                    for genre in track.genres:
                        if genre in genres:
                            genres[genre] += 1
                        else:
                            genres[genre] = 1
        
        # get the top artists and genres, weighted by rating and number of times they appear
        top_artists = []
        top_genres = []
        for artist in artists:
            top_artists.append((artist, artists[artist] * rating))
        for genre in genres:
            top_genres.append((genre, genres[genre] * rating))
        
        top_artists = sorted(top_artists, key = lambda artist: artist[1], reverse = True)
        top_genres = sorted(top_genres, key = lambda genre: genre[1], reverse = True)

        # get all tracks by the top artists and genres, alternating between artists and genres.
        for i in range(max(len(top_artists), len(top_genres))):
            if i < len(top_artists):
                output += self.get_tracks_from_artist(top_artists[i][0].artist_id)
            if i < len(top_genres):
                output += self.get_tracks_by_genre(top_genres[i][0].genre_id)

        # remove duplicates
        output = list(dict.fromkeys(output))

        # return the list of tracks
        return output
            
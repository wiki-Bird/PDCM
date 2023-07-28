from datetime import date
from typing import List

from sqlalchemy import desc, asc
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from sqlalchemy.orm import scoped_session

from music.domainmodel.album import Album
from music.domainmodel.artist import Artist
from music.domainmodel.genre import Genre
from music.domainmodel.review import Review
from music.domainmodel.track import Track
from music.domainmodel.user import User

from music.adapters.repository import AbstractRepository


class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()


class SqlAlchemyRepository(AbstractRepository):

    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    def add_album(self, album: Album):
        with self._session_cm as scm:
            scm.session.add(album)
            scm.commit()
        
    def add_artist(self, artist: Artist):
        with self._session_cm as scm:
            scm.session.add(artist)
            scm.commit()
    
    def add_genre(self, genre: Genre):
        with self._session_cm as scm:
            scm.session.add(genre)
            scm.commit()
    
    def add_playlist(self, playlist):
        pass

    def add_review(self, review: Review):
        with self._session_cm as scm:
            scm.session.add(review)
            scm.commit()

    def add_track(self, track: Track):
        with self._session_cm as scm:
            scm.session.add(track)
            scm.commit()
            if track.album:
                scm.session.execute(f'UPDATE tracks SET album_id = {track.album.album_id} WHERE track_id = {track.track_id}')
                if track.track_id == 554: print(f'UPDATE tracks SET album_id = {track.album.album_id} WHERE track_id = {track.track_id}')
            if track.artist:
                scm.session.execute(f'UPDATE tracks SET artist_id = {track.artist.artist_id} WHERE track_id = {track.track_id}')
                if track.track_id == 554: print(f'UPDATE tracks SET artist_id = {track.artist.artist_id} WHERE track_id = {track.track_id}')
            for genre in track.genres:
                scm.session.execute(f'INSERT INTO track_genres (track_id, genre_id) VALUES ({track.track_id}, {genre.genre_id})')
            scm.commit()
    
    def add_user(self, user: User):
        with self._session_cm as scm:
            scm.session.add(user)
            scm.commit()

    def track_id_to_class(self, track_id: int) -> Track:
        raw_track = self._session_cm.session.execute(
            f'SELECT \
            tracks.title, tracks.track_url, tracks.track_duration, tracks.image_file, \
            albums.album_id, albums.title, albums.album_url, albums.album_type, albums.release_year, \
            artists.artist_id, artists.full_name, tracks.track_file \
            FROM tracks \
            LEFT JOIN albums ON albums.album_id == tracks.album_id \
            LEFT JOIN artists on artists.artist_id == tracks.artist_id \
            WHERE track_id = {track_id}'
        ).fetchone()

        [title, url, duration, image_file, album_id, album_title, album_url, album_type, album_year, artist_id, artist_name, track_file] = raw_track

        track = Track(track_id, title)
        track.track_url = url; track.track_duration = duration; track.image_file = image_file; track.track_file = track_file

        if album_id:
            album = Album(album_id, album_title)
            album.album_url = album_url; album.album_type = album_type; album.release_year = album_year;
            track.album = album
        
        if artist_id:
            artist = Artist(artist_id, artist_name)
            track.artist = artist

        raw_genres = self._session_cm.session.execute(f'SELECT track_genres.genre_id, genres.genre_name FROM track_genres INNER JOIN genres ON genres.genre_id == track_genres.genre_id WHERE track_id = {track_id}').fetchall()

        for raw_genre in raw_genres:
            [id, name] = raw_genre
            genre = Genre(id, name)
            track.add_genre(genre)

        return track
        
    def get_tracks_sorted_by_album(self, reverse=False):
        tracks = self._session_cm.session.execute(f'SELECT tracks.track_id FROM tracks LEFT JOIN albums ON albums.album_id == tracks.album_id ORDER BY albums.title {"DESC" if reverse else "ASC"}').fetchall()
        return [self.track_id_to_class(track[0]) for track in tracks]
        

    def get_tracks_sorted_by_artist(self, reverse=False):
        tracks = self._session_cm.session.execute(f'SELECT tracks.track_id FROM tracks LEFT JOIN artists ON artists.artist_id == tracks.artist_id ORDER BY artists.full_name {"DESC" if reverse else "ASC"}').fetchall()
        return [self.track_id_to_class(track[0]) for track in tracks]

    def get_tracks_sorted_by_id(self, reverse=False):
        tracks = self._session_cm.session.execute(f'SELECT tracks.track_id FROM tracks ORDER BY tracks.track_id {"DESC" if reverse else "ASC"}').fetchall()
        return [self.track_id_to_class(track[0]) for track in tracks]

    def get_tracks_sorted_by_title(self, reverse=False):
        tracks = self._session_cm.session.execute(f'SELECT tracks.track_id FROM tracks ORDER BY tracks.title {"DESC" if reverse else "ASC"}').fetchall()
        return [self.track_id_to_class(track[0]) for track in tracks]
    
    def get_tracks_sorted_by_duration(self, reverse=False):
        tracks = self._session_cm.session.execute(f'SELECT tracks.track_id FROM tracks ORDER BY tracks.track_duration {"DESC" if reverse else "ASC"}').fetchall()
        return [self.track_id_to_class(track[0]) for track in tracks]
    
    def get_track(self, track_id: int):
        return self.track_id_to_class(track_id)

    def get_tracks_by_genre(self, genre_id: int):
        all_tracks_of_this_genre = self._session_cm.session.execute(
            f'SELECT tracks.track_id FROM tracks \
            INNER JOIN track_genres ON track_genres.track_id == tracks.track_id \
            INNER JOIN genres ON genres.genre_id == track_genres.genre_id \
            WHERE genres.genre_id == {genre_id}').fetchall()
        return [self.track_id_to_class(track[0]) for track in all_tracks_of_this_genre]

    def get_tracks_by_genres(self):
        all_genres = self._session_cm.session.execute('SELECT * FROM genres').fetchall()

        genre_tracks_map: dict[Genre, list[Track]] = {}

        for [genre_id, genre_name] in all_genres:
            genre = Genre(genre_id, genre_name)

            tracks_of_this_genre = self._session_cm.session.execute(
                f'SELECT tracks.track_id from tracks \
                INNER JOIN track_genres ON track_genres.track_id == tracks.track_id \
                WHERE track_genres.genre_id == {genre_id}')
            
            genre_tracks_map[genre] = [self.track_id_to_class(i[0]) for i in tracks_of_this_genre]

        return genre_tracks_map

    def get_genre(self, genre_id: int):
        [genre_id, genre_name] = self._session_cm.session.execute(f'SELECT * FROM genres WHERE genre_id = {genre_id}').fetchone()
        return Genre(genre_id, genre_name)
    
    def get_tracks_from_artist(self, artist_id: int):
        return [self.track_id_to_class(i[0]) for i in self._session_cm.session.execute(f'SELECT track_id FROM tracks WHERE artist_id = {artist_id}').fetchall()]
    
    def get_artist(self, artist_id: int):
        [id, name] = self._session_cm.session.execute(f'SELECT * FROM artists WHERE artist_id = {artist_id}').fetchone()
        return Artist(id, name)
    
    def get_tracks_from_album(self, album_id: int):
        all_track_ids = self._session_cm.session.execute(f'SELECT track_id FROM tracks WHERE album_id = {album_id}').fetchall()
        return [self.track_id_to_class(i[0]) for i in all_track_ids]
    
    def get_album(self, album_id: int):
        [id, title, url, type, year] = self._session_cm.session.execute(f'SELECT * FROM albums WHERE album_id = {album_id}').fetchone()

        album = Album(id, title)
        album.album_url = url
        album.album_type = type
        album.release_year = year

        return album
    
    def get_user(self, username: str):
        raw_user = self._session_cm.session.execute(f'SELECT * FROM users WHERE user_name = "{username}"').fetchone()
        if raw_user:
            [id, name, password] = raw_user
            return User(id, name, password)
        return None
        
    def get_reviews_of_track(self, track_id: int):
        raw_reviews = self._session_cm.session.execute(f'SELECT * FROM reviews WHERE track_id = {track_id}').fetchall()
        reviews: list[Review] = []
        for [text, rating, timestamp, author_name, track_id] in raw_reviews:
            track = self.track_id_to_class(track_id)
            review = Review(track, text, rating, author_name)
            review.__timestamp = timestamp
            reviews.append(review)
            
        return reviews
    
    def get_recommended_tracks(self, origin_track: Track):
        all_ids = self._session_cm.session.execute('SELECT track_id FROM tracks').fetchall()

        all_tracks = [self.track_id_to_class(i[0]) for i in all_ids]

        tracks = []
        for track in all_tracks:
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

        reviews = []
        
        # get all reviews by the user
        raw_reviews = self._session_cm.session.execute(
            f'SELECT reviews.track_id, reviews.review_text, reviews.rating, reviews.timestamp FROM reviews \
            INNER JOIN users ON users.user_name == reviews.author_name \
            WHERE users.user_name == "{user_name}"').fetchall()

        for raw_review in raw_reviews:
            [track_id, review_text, rating, timestamp] = raw_review

            track = self.track_id_to_class(track_id)

            review = Review(track, review_text, rating, user_name)
            review.__timestamp = timestamp
            reviews.append(review)


        # get all tracks reviewed by the user in a dictionary where the key is the track rating 1-5 and the value is a list of tracks with that rating
        tracks_by_rating = {}
        for raw_review in reviews:
            if raw_review.rating in tracks_by_rating:
                tracks_by_rating[raw_review.rating].append(raw_review.track)
            else:
                tracks_by_rating[raw_review.rating] = [raw_review.track]
        
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
            
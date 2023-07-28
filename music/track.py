from flask import Blueprint, render_template, request, session, redirect, url_for
import music.adapters.repository as repo

from flask_wtf import FlaskForm
from wtforms import HiddenField, TextAreaField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, ValidationError, NumberRange

from music.domainmodel.review import Review
from music.utilities.utilities import do_pagination


""" This blueprint encapsulates interactions relating to getting tracks of certain genre, artist, album; and singular tracks. """
track_blueprint = Blueprint(
    'track_bp', __name__, url_prefix='/track')

@track_blueprint.route('/<int:track_id>', methods=['GET'])
def track(track_id):
    track = repo.repo_instance.get_track(track_id)
    if track is None:
        return render_template('404.html')

    reviews = repo.repo_instance.get_reviews_of_track(track_id)
    print(len(reviews))

    existing_review = None

    if 'user_name' in session:
        for i in range(len(reviews)):
            if reviews[i].author_name == session['user_name']:
                existing_review = reviews[i]
                reviews.pop(i)
                break

    recommended_tracks = repo.repo_instance.get_recommended_tracks(track)

    return render_template('tracks/track.html', track=track, reviews=reviews, existing_review=existing_review, recommended_tracks=recommended_tracks)

@track_blueprint.route('/genres')
def genres():
    genres = repo.repo_instance.get_tracks_by_genres()
    tracks = repo.repo_instance.get_tracks_sorted_by_title()
    return render_template('tracks/genres.html', genres=genres, tracks=tracks)

@track_blueprint.route('/genre/<int:genre_id>')
def genre(genre_id):
    page_number = int(request.args.get('page') or '1')
    tracks = repo.repo_instance.get_tracks_by_genre(genre_id)
    genre = repo.repo_instance.get_genre(genre_id)
    (page, num_pages) = do_pagination(tracks, page_number)
    return render_template('tracks/genre.html', tracks=page, genre=genre, num_pages=num_pages, page_number=page_number, total_results=len(tracks))

@track_blueprint.route('/artist/<int:artist_id>')
def artist(artist_id):
    page_number = int(request.args.get('page') or '1')
    tracks = repo.repo_instance.get_tracks_from_artist(artist_id)
    artist = repo.repo_instance.get_artist(artist_id)
    (page, num_pages) = do_pagination(tracks, page_number)
    return render_template('tracks/artist.html', tracks=page, artist=artist, num_pages=num_pages, page_number=page_number, total_results=len(tracks))

@track_blueprint.route('/album/<int:album_id>')
def album(album_id):
    page_number = int(request.args.get('page') or '1')
    tracks = repo.repo_instance.get_tracks_from_album(album_id)
    album = repo.repo_instance.get_album(album_id)
    (page, num_pages) = do_pagination(tracks, page_number)
    return render_template('tracks/album.html', tracks=page, album=album, num_pages=num_pages, page_number=page_number, total_results=len(tracks))

@track_blueprint.route('/<int:track_id>/review', methods=['GET', 'POST'])
def review(track_id):
    try:
        user_name = session['user_name']
    except KeyError:
        return redirect(url_for('authentication_bp.login'))

    form = ReviewForm()
    track = repo.repo_instance.get_track(track_id)

    if form.validate_on_submit():
        review = Review(track, form.review_text.data, form.rating.data, user_name)
        repo.repo_instance.add_review(review)
        return redirect(url_for('track_bp.track', track_id=track_id))

    return render_template(
        'tracks/review.html',
        track=track,
        form=form,
        handler_url=url_for('track_bp.review', track_id=track_id)
    )

@track_blueprint.route('/discover')
def discover():
    try:
        user_name = session['user_name']
    except KeyError:
        return redirect(url_for('authentication_bp.login'))
    
    tracks = repo.repo_instance.get_recommended_tracks_for_user(user_name)
    return render_template('tracks/discover.html', tracks=tracks, user_name=user_name)
    

class ReviewForm(FlaskForm):
    review_text = TextAreaField('Review', [DataRequired(),
    Length(min=5, message='Your review is too short (minimum 5 characters)')])
    rating = IntegerField('Rating', [NumberRange(min=1, max=5, message="Rating must be between 1 and 5 (inclusive)")])
    submit = SubmitField("Submit")

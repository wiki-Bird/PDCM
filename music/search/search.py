from flask import Blueprint, render_template, request, session, redirect, url_for
import music.adapters.repository as repo

from flask_wtf import FlaskForm
from wtforms import HiddenField, TextAreaField, SubmitField, IntegerField, BooleanField
from wtforms.validators import DataRequired, Length, ValidationError, NumberRange

from music.domainmodel.review import Review
from music.search.services import filter_tracks_by_album, filter_tracks_by_artist, filter_tracks_by_genre, filter_tracks_by_title
from music.utilities.utilities import do_pagination


""" This blueprint encapsulates interactions relating to searching tracks by title, artist, genre, or album, as well as displaying those search results. """
search_blueprint = Blueprint(
    'search_bp', __name__)

@search_blueprint.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()

    genres = [i.name for i in repo.repo_instance.get_tracks_by_genres().keys() if i.name]
    genres.sort()

    results = []

    if form.validate_on_submit():
        results = repo.repo_instance.get_tracks_sorted_by_id()
        if form.artist.data: filter_tracks_by_artist(results, form.artist.data)
        if form.album.data: filter_tracks_by_album(results, form.album.data)
        if form.genre.data: filter_tracks_by_genre(results, form.genre.data)
        if form.title.data: filter_tracks_by_title(results, form.title.data, form.fuzzy_search.data)

    return render_template(
        'tracks/search.html',
        form=form,
        handler_url=url_for('search_bp.search'),
        results=results[:50],
        genres=genres,
        total_results=len(results)
    )


class SearchForm(FlaskForm):
    title = TextAreaField('Title')
    fuzzy_search = BooleanField('Fuzzy Search (Title Only)')
    artist = TextAreaField('Artist')
    album = TextAreaField('Album')
    genre = TextAreaField('Genre')
    submit = SubmitField()

from flask import Blueprint, render_template, request
import music.adapters.repository as repo
from music.search.services import filter_tracks_by_title
from music.utilities.utilities import do_pagination

""" This blueprint encapsulates interactions relating to getting all tracks, and searching for them. """
home_blueprint = Blueprint(
    'home_bp', __name__)

@home_blueprint.route('/', methods=['GET'])
def home():
    page_number = int(request.args.get('page') or '1')
    query = request.args.get('query')
    tracks = repo.repo_instance.get_tracks_sorted_by_id()

    if query:
        filter_tracks_by_title(tracks, query, True)

    (page, num_pages) = do_pagination(tracks, page_number)

    return render_template('home.html', tracks=page, num_pages=num_pages, page_number=page_number)

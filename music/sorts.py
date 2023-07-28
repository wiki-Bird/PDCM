from flask import Blueprint, render_template, request
import music.adapters.repository as repo
from music.utilities.utilities import do_pagination


""" This blueprint encapsulates interactions relating to getting sorted lists of tracks. """
sorts_blueprint = Blueprint(
    'sorts_bp', __name__)

@sorts_blueprint.route('/title', methods=['GET'])
def tracks_by_title():
    page_number = int(request.args.get('page') or '1')
    reverse = request.args.get('reverse') == 'true'
    tracks = repo.repo_instance.get_tracks_sorted_by_title(reverse)
    (page, num_pages) = do_pagination(tracks, page_number)
    return render_template('home.html', tracks=page, num_pages=num_pages, page_number=page_number, sort=f'title{int(reverse)}')

@sorts_blueprint.route('/artist', methods=['GET'])
def tracks_by_artist():
    page_number = int(request.args.get('page') or '1')
    reverse = request.args.get('reverse') == 'true'
    tracks = repo.repo_instance.get_tracks_sorted_by_artist(reverse)
    (page, num_pages) = do_pagination(tracks, page_number)
    return render_template('home.html', tracks=page, num_pages=num_pages, page_number=page_number, sort=f'artist{int(reverse)}')

@sorts_blueprint.route('/album', methods=['GET'])
def tracks_by_album():
    page_number = int(request.args.get('page') or '1')
    reverse = request.args.get('reverse') == 'true'
    tracks = repo.repo_instance.get_tracks_sorted_by_album(reverse)
    (page, num_pages) = do_pagination(tracks, page_number)
    return render_template('home.html', tracks=page, num_pages=num_pages, page_number=page_number, sort=f'album{int(reverse)}')

@sorts_blueprint.route('/duration', methods=['GET'])
def tracks_by_duration():
    page_number = int(request.args.get('page') or '1')
    reverse = request.args.get('reverse') == 'true'
    tracks = repo.repo_instance.get_tracks_sorted_by_duration(reverse)
    (page, num_pages) = do_pagination(tracks, page_number)
    return render_template('home.html', tracks=page, num_pages=num_pages, page_number=page_number, sort=f'duration{int(reverse)}')

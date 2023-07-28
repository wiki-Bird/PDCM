import math
from flask import Blueprint
from music.domainmodel.track import Track

""" This blueprint contains functions for doing pagination on lists of tracks. """
utilities_blueprint = Blueprint(
    'utilities_bp', __name__
)

"""
Extracts a page of results from a list of tracks.

Returns a tuple containing (in order):
    - The new list/page of tracks.
    - Total number of pages.

Page number should use 1-based indexing.
"""
def do_pagination(tracks: list[Track], page_number: int, per_page: int = 50):
    page_number -= 1
    num_pages = math.ceil(len(tracks) / per_page)
    page = tracks[page_number * per_page: (page_number + 1) * per_page]

    return (page, num_pages)

from flask import Blueprint, render_template, request
import music.adapters.repository as repo

""" This blueprint encapsulates interactions relating to getting tracks of certain genre, artist, album; and singular tracks. """
sorts_blueprint = Blueprint(
    'track_bp', __name__)
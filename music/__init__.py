"""Initialize Flask app."""

from pathlib import Path
from flask import Flask, render_template
from music.adapters.memory_repository import MemoryRepository
import music.adapters.repository as repo
from music.adapters import database_repository, repository_populate, orm
from music.adapters.orm import metadata, map_model_to_tables
import random

from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker, clear_mappers
from sqlalchemy.pool import NullPool


def create_app(test_config=None):
    app = Flask(__name__)

    app.config.from_object('config.Config')
    data_path = Path('music') / 'adapters' / 'data'

    if test_config is not None:
        app.config.from_mapping(test_config)
        data_path = app.config['TEST_DATA_PATH']

    if app.config['REPOSITORY'] == 'memory':
        repo.repo_instance = MemoryRepository()
        repository_populate.populate(data_path, repo.repo_instance)
    elif app.config['REPOSITORY'] == 'database':
        database_uri = app.config['SQLALCHEMY_DATABASE_URI']

        database_echo = app.config['SQLALCHEMY_ECHO']

        database_engine = create_engine(database_uri, connect_args={"check_same_thread": False}, poolclass=NullPool, echo=database_echo)

        session_factory = sessionmaker(autocommit=False, autoflush=True, bind=database_engine)

        repo.repo_instance = database_repository.SqlAlchemyRepository(session_factory)

        if app.config['TESTING'] == 'True' or len(database_engine.table_names()) == 0:
            print("REPOPULATING DATABASE...")

            clear_mappers()
            metadata.create_all(database_engine)  
            for table in reversed(metadata.sorted_tables):
                database_engine.execute(table.delete())

            map_model_to_tables()

            repository_populate.populate(data_path, repo.repo_instance)
            print("REPOPULATING DATABASE... FINISHED")

        else:
            map_model_to_tables()

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.template_filter('shuffle')
    def shuffle_filter(s):
        try:
            output = list(s)
            random.shuffle(output)
            return output
        except:
            return s

    with app.app_context():
        from .sorts import sorts_blueprint
        app.register_blueprint(sorts_blueprint)

        from .home import home_blueprint
        app.register_blueprint(home_blueprint)

        from .utilities import utilities
        app.register_blueprint(utilities.utilities_blueprint)

        from .authentication import authentication
        app.register_blueprint(authentication.authentication_blueprint)
    
        from .track import track_blueprint
        app.register_blueprint(track_blueprint)

        from .search import search
        app.register_blueprint(search.search_blueprint)

    @app.before_request
    def before_flask_http_request_function():
        if isinstance(repo.repo_instance, database_repository.SqlAlchemyRepository):
            repo.repo_instance.reset_session()

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        if isinstance(repo.repo_instance, database_repository.SqlAlchemyRepository):
            repo.repo_instance.close_session()

    return app

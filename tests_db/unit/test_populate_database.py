from sqlalchemy import select, inspect
from music.adapters.orm import metadata

def test_database_populate_inspect_table_names(database_engine):
    inspector = inspect(database_engine)
    assert inspector.get_table_names() == ['album', 'artist', 'genre', 'track']

def test_database_populate_select_all_from_album(database_engine):
    inspector = inspect(database_engine)
    name_of_album_table = inspector.get_table_names()[0]

    with database_engine.connect() as connection:
        result = connection.execute(select([name_of_album_table]))
        assert result.rowcount == 0


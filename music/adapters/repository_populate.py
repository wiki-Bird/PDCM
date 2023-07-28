from pathlib import Path
from music.adapters.csvdatareader import TrackCSVReader
from music.adapters.memory_repository import MemoryRepository

def populate(data_path: Path, repo: MemoryRepository):
    albums_file_name = str(data_path / 'raw_albums_excerpt.csv')
    tracks_file_name = str(data_path / 'raw_tracks_excerpt.csv')
    reader = TrackCSVReader(albums_file_name, tracks_file_name)
    reader.read_csv_files()

    [repo.add_album(i) for i in reader.dataset_of_albums]
    [repo.add_artist(i) for i in reader.dataset_of_artists]
    [repo.add_genre(i) for i in reader.dataset_of_genres]
    [repo.add_track(i) for i in reader.dataset_of_tracks]

from music.domainmodel.track import Track

def filter_tracks_by_artist(tracks: list[Track], artist: str):
    artist = artist.lower()
    for i in range(len(tracks) - 1, -1, -1):
        if not tracks[i].artist: tracks.pop(i)
        elif not tracks[i].artist.full_name: tracks.pop(i)
        elif tracks[i].artist.full_name.lower() != artist: tracks.pop(i)

def filter_tracks_by_album(tracks: list[Track], album: str):
    album = album.lower()
    for i in range(len(tracks) - 1, -1, -1):
        if not tracks[i].album: tracks.pop(i)
        elif not tracks[i].album.title: tracks.pop(i)
        elif tracks[i].album.title.lower() != album: tracks.pop(i)
    
def filter_tracks_by_genre(tracks: list[Track], genre: str):
    genre = genre.lower()
    for i in range(len(tracks) - 1, -1, -1):
        track_genres = [i.name.lower() for i in tracks[i].genres if i.name]
        if not genre in track_genres: tracks.pop(i)

def filter_tracks_by_title(tracks: list[Track], title: str, fuzzy: bool, min_similarity: float = 0.5):
    title = title.lower()

    if fuzzy:
        for i in range(len(tracks) - 1, -1, -1):
            if not tracks[i].title: tracks.pop(i)
            elif levenshtein_distance(tracks[i].title.lower(), title) < min_similarity:
                tracks.pop(i)
    else:
        for i in range(len(tracks) - 1, -1, -1):
            if not tracks[i].title: tracks.pop(i)
            elif tracks[i].title.lower() != title: tracks.pop(i)


""" Compares the similarity between 2 strings using Levenshtein distance. """
def levenshtein_distance(str1: str, str2: str) -> float:
    longerStr = str1
    shorterStr = str2
    if len(str1) < len(str2):
        longerStr = str2
        shorterStr = str1
    
    longerLen = len(longerStr)
    if longerLen == 0: return 1.0 # both strings are "", so perfect match (1.0)

    return (longerLen - edit_distance(longerStr, shorterStr)) / longerLen

"""
A helper function for levenshtein_distance.

Returns the distance (or 'cost') to edit s1 into s2.
"""
def edit_distance(s1: str, s2: str) -> float:
    s1 = s1.lower()
    s2 = s2.lower()

    costs: list[float] = []

    for _ in range(len(s2) + 1):
        costs.append(0)

    for i in range(len(s1) + 1):
        lastVal = i

        for j in range(len(s2) + 1):
            if i == 0: costs[j] = j
            elif j > 0:
                newVal = costs[j - 1]

                if s1[i - 1] != s2[j - 1]:
                    newVal = min(min(newVal, lastVal), costs[j]) + 1
                
                costs[j - 1] = lastVal
                lastVal = newVal

        if i > 0: costs[len(s2)] = lastVal
    
    return costs[len(s2)]

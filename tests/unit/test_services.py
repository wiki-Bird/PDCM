from music.search.services import levenshtein_distance

def test_levenshtein_distance():
    # identical strings should be 1.0
    assert levenshtein_distance('', '') == 1
    assert levenshtein_distance('reallylongstring', 'reallylongstring') == 1

    # completely different strings should be 0.0
    assert levenshtein_distance('', 'a') == 0
    assert levenshtein_distance('liam', 'ty') == 0
    assert levenshtein_distance('pog', 'champ') == 0

    # expected magic number values
    assert levenshtein_distance('louder', 'faster') == 1 / 3
    assert levenshtein_distance('monday', 'sunday') == 2 / 3
    assert levenshtein_distance('sitting', 'kitten') == 0.5714285714285714

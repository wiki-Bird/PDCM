from music.utilities.utilities import do_pagination

def test_pagination():
    my_list = [0, 1, 2, 3, 4, 5, 6, 7, 8]

    # page 0 should always be an empty list
    assert do_pagination(my_list, 0) == ([], 1)

    # different page sizes
    assert do_pagination(my_list, 1, 3) == ([0, 1, 2], 3)
    assert do_pagination(my_list, 1, 6) == ([0, 1, 2, 3, 4, 5], 2)
    assert do_pagination(my_list, 1, 9) == (my_list, 1)

    # different page numbers
    assert do_pagination(my_list, 2, 3) == ([3, 4, 5], 3)
    assert do_pagination(my_list, 3, 3) == ([6, 7, 8], 3)

    assert do_pagination(my_list, 2, 6) == ([6, 7, 8], 2)

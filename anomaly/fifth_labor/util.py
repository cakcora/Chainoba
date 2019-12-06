import sys

import pyprind


def progress_bar(title, max_value):
    """
    initialize the progress bar
    :param title:
    :param max_value:
    :return: ProgBar
    """

    bar = pyprind.ProgBar(max_value, stream=sys.stdout, title=title, bar_char='.')
    return bar

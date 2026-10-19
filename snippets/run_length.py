from itertools import groupby


def rle(seq, key=None):
    return [(k, len(list(g))) for k, g in groupby(seq, key=key)]

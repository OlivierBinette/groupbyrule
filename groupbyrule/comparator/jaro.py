from .comparator import StringComparator

import numpy as np


def common(s, t, window):
    k = min(len(s), len(t))


def transpositions(sp, tp):
    pass


def jaro(s, t):
    pass


class Jaro(StringComparator):

    def __init__(self, normalize=True, similarity=False):
        self.normalize = normalize
        self.similarity = similarity

    def compare(self, s1, s2):
        pass

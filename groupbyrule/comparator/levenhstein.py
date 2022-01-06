import numpy as np
from .comparator import Comparator


def _levenshtein(s, t, dmat):
    m = len(s)
    n = len(t)
    dmat[:, 0] = np.arange(dmat.shape[0])
    dmat[0, :] = np.arange(2)

    for j in range(1, n+1):
        dmat[0, (j-1) % 2] = j-1
        dmat[0, j % 2] = j
        for i in range(1, m+1):
            cost = 0
            if s[i-1] != t[j-1]:
                cost = 1
            dmat[i, j % 2] = min(dmat[i-1, j % 2] + 1, dmat[i, (j-1) % 2] +
                                 1, dmat[i-1, (j-1) % 2] + cost)
    return dmat[m, n % 2]


class Levenshtein(Comparator):

    def __init__(self, normalize=True, dmat_size=100):
        self.dmat = np.zeros((dmat_size, 2))
        self.normalize = normalize

    def compare(self, s1, s2):
        if self.normalize:
            return _levenshtein(s1, s2, self.dmat) / max(len(s1), len(s2))
        return _levenshtein(s1, s2, self.dmat)

    def elementwise(self, l1, l2):
        return np.array([[_levenshtein(s, t, self.dmat) for t in l2] for s in l1])

import numpy as np


def _levenshtein(s, t, dmat):
    m = len(s)
    n = len(t)
    dmat[:, 0] = np.arange(dmat.shape[0])
    dmat[0, :] = np.arange(dmat.shape[1])

    for j in range(1, n+1):
        for i in range(1, m+1):
            cost = 0
            if s[i-1] != t[j-1]:
                cost = 1
            dmat[i, j] = min(dmat[i-1, j] + 1, dmat[i, j-1] +
                             1, dmat[i-1, j-1] + cost)
    return dmat[m, n]


class Levenshtein:
    def __init__(self, dmat_size=100):
        self.dmat = np.zeros((dmat_size, dmat_size))

    def compare(self, s1, s2):
        return _levenshtein(s1, s2, self.dmat)

    def elementwise(self, l1, l2):
        return np.array([[_levenshtein(s, t, self.dmat) for t in l2] for s in l1])

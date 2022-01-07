from .comparator import Comparator

import numpy as np


def _lcs(s, t, dmat):
    m = len(s)
    n = len(t)
    dmat[:, 0] = np.zeros(dmat.shape[0])

    for j in range(1, n+1):
        dmat[0, (j-1) % 2] = 0
        dmat[0, j % 2] = 0
        for i in range(1, m+1):
            cost = 0
            if s[i-1] != t[j-1]:
                dmat[i, j % 2] = max(dmat[i, (j-1) % 2], dmat[i-1, j % 2])
            else:
                dmat[i, j % 2] = dmat[i-1, (j-1) % 2] + 1

    return dmat[m, n % 2]


class LCSDistance(Comparator):

    def __init__(self, normalize=True, dmat_size=100):
        self.dmat = np.zeros((dmat_size, 2))
        self.normalize = normalize

    def compare(self, s1, s2):
        dist = len(s1) + len(s2) - 2 * _lcs(s1, s2, self.dmat)
        if self.normalize:
            return 2 * dist / (len(s1) + len(s2) + dist)
        return dist

    def elementwise(self, l1, l2):
        return np.array([[_lcs(s, t, self.dmat) for t in l2] for s in l1])

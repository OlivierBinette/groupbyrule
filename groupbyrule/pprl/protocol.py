from abc import ABC, abstractmethod
import numpy as np


class Protocol(ABC):

    def __init__(self, *actors):
        pass

    @abstractmethod
    def execute(self):
        pass


class BloomFilterThreshold(Protocol):

    QUERY_KWDS = ["bloom-filter"]

    def __init(self, *actors, threshold):
        self.actors = actors

    def execute(self):
        vectors = np.array([actor.query("bloom-filters")
                            for actor in self.actors])
        # Compute pairwise similarities
        # Threshold
        # Cluster
        raise NotImplementedError

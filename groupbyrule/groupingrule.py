from __future__ import annotations
import pandas as pd
import numpy as np
import igraph
from abc import ABC, abstractmethod

class GroupingRule(ABC):
    def __init__(self):
        self._graph: igraph.Graph = None
        self._groups: np.ndarray = None
        self.n: int = None
        self.index: pd.Index = None

        self._update_graph: bool = False
        self._update_groups: bool = False


    def fit(self, df: pd.DataFrame) -> GroupingRule:
        self.n = df.shape[0]
        self.index = df.index

        return self

    def __call__(self, index):
        return self.groups[index]

    @property
    @abstractmethod
    def graph(self) -> igraph.Graph:
        pass

    @property
    @abstractmethod
    def groups(self) -> np.ndarray:
        pass

from __future__ import annotations
import pandas as pd
import numpy as np
import igraph
from abc import ABC, abstractmethod
import numpy.typing as npt


GroupsType = npt.ArrayLike


class GroupingRule(ABC):
    def __init__(self):
        self._graph: igraph.Graph = None
        self._groups: GroupsType = None
        self.n: int = None
        self.index: pd.Index = None

        self._update_graph: bool = False
        self._update_groups: bool = False

    def fit(self, df: pd.DataFrame) -> GroupingRule:
        self.n = df.shape[0]
        self.index = df.index

        return self

    @property
    @abstractmethod
    def graph(self) -> igraph.Graph:
        pass

    @property
    @abstractmethod
    def groups(self) -> GroupsType:
        pass

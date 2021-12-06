from __future__ import annotations
import pandas as pd
import numpy as np
import igraph

from .groupingrule import GroupingRule
from .match import Match

class Any(GroupingRule):

    def __init__(self, *args):
        super().__init__()

        def parse_arg(arg):
            if isinstance(arg, str):
                return Match(arg)
            return arg
        self.rules = [parse_arg(arg) for arg in args]

    def apply(self, df: pd.DataFrame) -> Any:
        super().apply(df)
        graphs = [rule.apply(df).graph for rule in self.rules]
        self._graph = igraph.union(graphs, byname=False)
        self._update_clusters = True
        self._update_groups = True

        return self


    @property
    def graph(self):
        return self._graph

    @property
    def groups(self):
        if self._update_groups:
            self._groups_vector = self.clusters.groups
        return self._groups_vector

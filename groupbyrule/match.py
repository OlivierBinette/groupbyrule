from __future__ import annotations
import pandas as pd
import numpy as np
import igraph
import itertools

from .groupingrule import GroupingRule

class Match(GroupingRule):
    def __init__(self, *args):
        super().__init__()
        self.rules = args

    def apply(self, df: pd.DataFrame) -> Match:
        super().apply(df)

        if len(self.rules) == 0:
            if isinstance(self.rules[0], str):
                self._groups_vector = df.groupby(self.rules).ngroup().values
            elif isinstance(self.rules[0], GroupingRule):
                self._groups_vector = self.rules[0].apply(df).groups
            else:
                raise NotImplementedError()
        else:
            self._groups_vector = Match._groups_from_rules(self.rules, df)
        self._update_graph = True
        self._update_clusters = True
        self.n = df.shape[0]

        return self

    @staticmethod 
    def _groups_from_rules(rules, df: pd.DataFrame) -> np.ndarray:
        def _groups(rule, df):
            if isinstance(rule, str):
                return df.groupby(rule).ngroup().values
            elif isinstance(rule, GroupingRule):
                return rule.apply(df).groups
            else:
                raise NotImplementedError()
        return df.groupby([_groups(rule, df) for rule in rules]).ngroup().values

    @property
    def graph(self) -> igraph.Graph:
        if self._update_graph:
            clust = pd.DataFrame({"groups":self.groups}).groupby("groups").indices
            self._graph = igraph.Graph(n=self.n)
            self._graph.add_edges(itertools.chain(*(list(itertools.combinations(clust[x], 2)) for x in clust)))

        return self._graph

    @property
    def groups(self) -> np.ndarray:
        return self._groups_vector


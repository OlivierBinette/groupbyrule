from __future__ import annotations
from os import stat
import pandas as pd
import numpy as np
import igraph
from abc import ABC, abstractmethod
import itertools
from typing import Iterable
import numpy.typing as npt

from .groupingrule import GroupingRule, GroupsType


# TODO: Include "level" argument
class Match(GroupingRule):
    def __init__(self, *args):
        super().__init__()
        self.rules = args

    def fit(self, df: pd.DataFrame) -> Match:
        super().fit(df)

        self._groups = Match._groups_from_rules(self.rules, df)
        self._update_graph = True
        self._update_clusters = True
        self.n = df.shape[0]

        return self

    @staticmethod
    def _groups_from_rules(rules, df: pd.DataFrame) -> GroupsType:
        def _groups(rule, df):
            if isinstance(rule, str):
                I = pd.isna(df[rule].values)
                arr = np.ma.masked_array(df[rule].values, I)
                arr = np.unique(arr, return_inverse=True)[1]  # Get unique IDs
                # Set different IDs for NA values
                arr[I] = np.array(np.arange(len(arr), len(arr)+sum(I)))
                return arr
                # return df.groupby(rule).ngroup().values # Does not properly account for NA values
            elif isinstance(rule, GroupingRule):
                return rule.fit(df).groups
            else:
                raise NotImplementedError()

        arr = np.array([_groups(rule, df) for rule in rules]).T
        I = np.any(pd.isna(arr), axis=1)
        ids = np.unique(arr[~I, :], axis=0, return_inverse=True)[1]
        res = np.arange(arr.shape[0])
        res[~I] = ids
        return res
        # return df.groupby([_groups(rule, df) for rule in rules]).ngroup().values #Does not properly account for NA values

    @property
    def graph(self) -> igraph.Graph:
        if self._update_graph:
            clust = pd.DataFrame({"groups": self.groups}
                                 ).groupby("groups").indices
            self._graph = igraph.Graph(n=self.n)
            self._graph.add_edges(itertools.chain(
                *(list(itertools.combinations(clust[x], 2)) for x in clust)))  # This is slow
            self._update_graph = False
        return self._graph

    @property
    def groups(self) -> GroupsType:
        return self._groups


class All(GroupingRule):

    def __init__(self, *args):
        super().__init__()

        def parse_arg(arg):
            if isinstance(arg, str):
                return Match(arg)
            return arg
        self.rules = [parse_arg(arg) for arg in args]

    def fit(self, df: pd.DataFrame) -> All:
        super().fit(df)
        graphs = [rule.fit(df).graph for rule in self.rules]
        self._graph = igraph.intersection(graphs, byname=False)
        self._update_clusters = True
        self._update_groups = True

        return self

    @property
    def graph(self):
        return self._graph

    @property
    def groups(self):
        if self._update_groups:
            self._groups = self._graph.clusters().membership
            self._update_groups = False
        return self._groups


# TODO: Include "level" argument to fix slowness at graph level
# TODO: Add blocking option
class Any(GroupingRule):

    def __init__(self, *args):
        super().__init__()

        def parse_arg(arg):
            if isinstance(arg, str):
                return Match(arg)
            return arg
        self.rules = [parse_arg(arg) for arg in args]

    def fit(self, df: pd.DataFrame) -> Any:
        super().fit(df)
        # Slow; might be better to work at the groups level
        graphs = [rule.fit(df).graph for rule in self.rules]
        self._graph = igraph.union(graphs, byname=False)
        self._update_clusters = True
        self._update_groups = True

        return self

    @staticmethod
    def combine_graphs(graphs: Iterable[igraph.Graph]) -> igraph.Graph:
        pass

    @staticmethod
    def combine_groups(groups: Iterable[GroupsType]) -> GroupsType:
        pass

    @property
    def graph(self):
        return self._graph

    @property
    def groups(self):
        if self._update_groups:
            self._groups = self._graph.clusters().membership
            self._update_groups = False
        return self._groups


class AllButK(Any):

    def __init__(self, *args, k=0, level="groups"):
        if level == "groups":
            rules = [Match(*x)
                     for x in itertools.combinations(args, len(args)-k)]
        elif level == "graph":
            rules = [All(*x)
                     for x in itertools.combinations(args, len(args)-k)]
        super().__init__(*rules)

        # Code below is very inefficient when there are large clusters in some of the *args rule
        # def parse_arg(arg):
        #     if isinstance(arg, str):
        #         return Match(arg)
        #     return arg
        # self.rules = [parse_arg(arg) for arg in args]
        # self.k = k

    # def fit(self, df: pd.DataFrame) -> AllButK:
    #     super().fit(df)
    #     graphs = [rule.fit(df).graph for rule in self.rules]
    #     base_graph = graphs[0].copy()
    #     if len(graphs) >= 2:
    #         for graph in itertools.islice(graphs, 1, None):
    #             print("test")
    #             base_graph.add_edges([(e.source, e.target) for e in graph.es])
    #     I = np.where(np.array(base_graph.es.count_multiple()) < len(graphs) - self.k)[0]
    #     base_graph.delete_edges(base_graph.es.select(I))
    #     base_graph.simplify()

    #     self._graph = base_graph
    #     self._update_clusters = True
    #     self._update_groups = True

    #     return self

    # @property
    # def graph(self):
    #     return self._graph

    # @property
    # def groups(self):
    #     if self._update_groups:
    #         self._groups = self._graph.clusters().membership
    #         self._update_groups = False
    #     return self._groups

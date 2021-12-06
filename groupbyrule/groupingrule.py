from __future__ import annotations
import pandas as pd
import numpy as np
import igraph
from abc import ABC, abstractmethod
import itertools

class GroupingRule(ABC):
    def __init__(self):
        self._graph: igraph.Graph = None
        self._groups: np.ndarray = None
        self.n: int = None
        self.index: pd.Index = None

        self._update_graph: bool = False
        self._update_groups: bool = False


    def apply(self, df: pd.DataFrame) -> GroupingRule:
        self.n = df.shape[0]
        self.index = df.index

        return self

    @property
    @abstractmethod
    def graph(self) -> igraph.Graph:
        pass

    @property
    @abstractmethod
    def groups(self) -> np.ndarray:
        pass

class Match(GroupingRule):
    def __init__(self, *args):
        super().__init__()
        self.rules = args

    def apply(self, df: pd.DataFrame) -> Match:
        super().apply(df)

        self._groups = Match._groups_from_rules(self.rules, df)
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
            self._update_graph = False
        return self._graph

    @property
    def groups(self) -> np.ndarray:
        return self._groups

class All(GroupingRule):

    def __init__(self, *args):
        super().__init__()

        def parse_arg(arg):
            if isinstance(arg, str):
                return Match(arg)
            return arg
        self.rules = [parse_arg(arg) for arg in args]

    def apply(self, df: pd.DataFrame) -> All:
        super().apply(df)
        graphs = [rule.apply(df).graph for rule in self.rules]
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
            self._groups = self._graph.clusters().membership
            self._update_groups = False
        return self._groups


class AllButK(Any):

    def __init__(self, *args, k=0, level="groups"):
        if level == "groups":
            rules = [Match(*x) for x in itertools.combinations(args, len(args)-k)]
        elif level == "graph":
            rules = [All(*x) for x in itertools.combinations(args, len(args)-k)]
        super().__init__(*rules)

        # def parse_arg(arg):
        #     if isinstance(arg, str):
        #         return Match(arg)
        #     return arg
        # self.rules = [parse_arg(arg) for arg in args]
        # self.k = k

    # def apply(self, df: pd.DataFrame) -> AllButK:
    #     super().apply(df)
    #     graphs = [rule.apply(df).graph for rule in self.rules]
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

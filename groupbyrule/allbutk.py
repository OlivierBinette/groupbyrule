from __future__ import annotations
import pandas as pd
import numpy as np
import igraph
import itertools

from .groupingrule import GroupingRule
from .match import Match
from .any import Any

class AllButK(Any):

    def __init__(self, *args, k=0):
        rules = [Match(*x) for x in itertools.combinations(args, len(args)-k)]
        super().__init__(Any(*rules))

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

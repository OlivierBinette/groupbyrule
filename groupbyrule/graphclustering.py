from .linkagerule import LinkageRule
import numpy as np
import pandas as pd
from match import graph_from_groups


def connected_components(graph):
    return graph.clusters().membership


class ConnectedComponents(LinkageRule):

    def __init__(self, rule):
        self.rule = rule
        self._groups = None
        self._graph = None
        self._update_graph = False

    def fit(self, df):
        self._groups = connected_components(self.rule.fit(df).graph)
        self._update_graph = True

    @property
    def groups(self):
        return self._groups

    @property
    def graph(self):
        if self._update_graph:
            self.graph = graph_from_groups(self._groups)
            self._update_graph = False
        return self._graph


class

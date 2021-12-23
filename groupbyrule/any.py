from .linkagerule import LinkageRule
from .match import _groups
import pandas as pd
from igraph import Graph
import igraph
import itertools


def pairwise(iterable):
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)


def _path_graph(rule, df):
    gr = rule.fit(df).groups
    clust = pd.DataFrame({"groups": gr}
                         ).groupby("groups").indices
    graph = Graph(n=df.shape[0])
    graph.add_edges(itertools.chain(
        *(list(pairwise(clust[x])) for x in clust)))

    return graph


class Any(LinkageRule):
    def __init__(self, *args):
        self.rules = args
        self._graph = None
        self._groups = None
        self._update_groups = False
        self.n = None

    def fit(self, df):
        self.update_groups = True
        graphs_vect = [_path_graph(rule, df) for rule in self.rules]
        self._graph = igraph.union(graphs_vect)
        return self

    @property
    def groups(self):
        if self.update_groups:
            self.update_groups = False
            self._groups = self._graph.clusters().membership
        return self._groups

    @property
    def graph(self) -> Graph:
        return self._graph

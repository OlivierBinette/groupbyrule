from numpy import intc
from .linkagerule import LinkageRule
from .match import _groups
import pandas as pd
from igraph import Graph
import igraph
import itertools
import numpy as np


class Any(LinkageRule):
    """
    Class representing the logical disjunction of linkage rules.

    Attributes
    ----------
    graph: igraph.Graph
        Graph representing linkage fitted to the data. Defaults to None and is instanciated after the `fit()` function is called.

    groups: integer array
        Membership vector for the linkage clusters fitted to the data. Defaults to None and is instanciated after the `fit()` function is called.

    Methods
    -------
    fit(df)
        Fits linkage rule to the given dataframe.
    """

    def __init__(self, *args):
        """
        Parameters
        ----------
        args: list containing strings and/or LinkageRule objects.
            The `Any` object represents the logical disjunction of the set of rules given by `args`. 
        """
        self.rules = args
        self._graph = None
        self._groups = None
        self._update_groups = False

    def fit(self, df):
        self._update_groups = True
        graphs_vect = [_path_graph(rule, df) for rule in self.rules]
        self._graph = igraph.union(graphs_vect)
        return self

    @ property
    def groups(self):
        if self._update_groups:
            self._update_groups = False
            self._groups = np.array(
                self._graph.clusters().membership)
        return self._groups

    @ property
    def graph(self) -> Graph:
        return self._graph


def pairwise(iterable):
    """
    Iterate over consecutive pairs:
        s -> (s[0], s[1]), (s[1], s[2]), (s[2], s[3]), ...

    Note
    ----
    Current implementation is from itertools' recipes list available at https://docs.python.org/3/library/itertools.html
    """
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)


def _path_graph(rule, df):
    """
    Compute path graph corresponding to the rule's clustering: cluster elements are connected as a path.

    Parameters
    ----------
    rule: string or LinkageRule
        Linkage rule for which to compute the corresponding path graph (strings are interpreted as exact matching rules for the corresponding column).
    df: DataFrame
        Data to which the linkage rule is fitted.

    Returns
    -------
    Graph object such that nodes in the same cluster (according to the fitted linkage rule) are connected as graph paths.
    """
    gr = _groups(rule, df)
    clust = pd.DataFrame({"groups": gr}
                         ).groupby("groups").indices
    graph = Graph(n=df.shape[0])
    graph.add_edges(itertools.chain.from_iterable(
        pairwise(clust[x]) for x in clust))

    return graph

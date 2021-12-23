import pandas as pd
import numpy as np
import itertools
from igraph import Graph
from .groupingrule import LinkageRule


def _groups(rule, df):
    """
    Fit linkage rule to dataframe and return membership vector.

    Parameters
    ----------
    rule: string or LinkageRule
        Linkage rule to be fitted to the data. If `rule` is a string, then this is interpreted as an exact matching rule for the corresponding column.
    df: DataFrame
        pandas Dataframe to which the rule is fitted.

    Returns
    -------
    Membership vector (i.e. integer vector) u such that u[i] indicates the cluster to which dataframe row i belongs. 

    Notes
    -----
    NA values are considered to be non-matching.

    Examples
    --------
    >>> import pandas as pd
    >>> df = pd.DataFrame({"fname":["Olivier", "Jean-Francois", "Alex"], "lname":["Binette", "Binette", pd.NA]})

    Groups specified by distinct first names:
    >>> _groups("fname", df)
    array([2, 1, 0], dtype=int8)

    Groups specified by same last names:
    >>> _groups("lname", df)
    array([0, 0, 3], dtype=int8)

    Groups specified by a given linkage rule:
    >>> rule = Match("fname")
    >>> _groups(rule, df)
    array([2, 1, 0], dtype=int8)
    """
    if (isinstance(rule, str)):
        arr = np.copy(pd.Categorical(df[rule]).codes)
        I = (arr == -1)  # NA value indicators
        arr[I] = np.arange(len(arr), len(arr)+sum(I))
        return arr
    elif isinstance(rule, LinkageRule):
        return rule.fit(df).groups
    else:
        raise NotImplementedError()


def _groups_from_rules(rules, df):
    """
    Fit linkage rules to data and return groups corresponding to their logical conjunction.

    This function computes the logical conjunction of a set of rules, operating at the groups level. That is, rules are fitted to the data, membership vector are obtained, and then the groups specified by these membership vectors are intersected.

    Parameters
    ----------
    rules: list[LinkageRule]
        List of strings or Linkage rule objects to be fitted to the data. Strings are interpreted as exact matching rules on the corresponding columns.

    df: DataFrame
        pandas DataFrame to which the rules are fitted.

    Returns
    -------
    Membership vector representing the cluster to which each dataframe row belongs.

    Notes
    -----
    NA values are considered to be non-matching.

    Examples
    --------
    >>> import pandas as pd
    >>> df = pd.DataFrame({"fname":["Olivier", "Jean-Francois", "Alex"], "lname":["Binette", "Binette", pd.NA]})
    >>> _groups_from_rules(["fname", "lname"], df)
    array([2, 1, 0])
    """

    arr = np.array([_groups(rule, df) for rule in rules]).T
    groups = np.unique(arr, axis=0, return_inverse=True)[1]
    return groups


class Match(LinkageRule):
    """
    Class representing an exact matching rule over a given set of columns.

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

    Examples
    --------
    >>> import pandas as pd
    >>> df = pd.DataFrame({"fname":["Olivier", "Jean-Francois", "Alex"], "lname":["Binette", "Binette", pd.NA]})

    Link records which agree on both the "fname" and "lname" fields.
    >>> rule = Match("fname", "lname")

    Fit linkage rule to the data.
    >>> rule.fit(df)

    Construct deduplicated dataframe, retaining only the first record in each cluster.
    >>> df.groupby(rule.groups).first()
    """

    def __init__(self, *args):
        """
        Parameters
        ----------
        args: list containing strings and/or LinkageRule objects.
            The `Match` object represents the logical conjunction of the set of rules given in the `args` parameter. 
        """
        self.rules = args
        self._update_graph = False
        self.n = None

    def fit(self, df):
        self._groups = _groups_from_rules(self.rules, df)
        self._update_graph = True
        self.n = df.shape[0]

        return self

    @property
    def groups(self):
        return self._groups

    @property
    def graph(self) -> Graph:
        if self._update_graph:
            clust = pd.DataFrame({"groups": self.groups}
                                 ).groupby("groups").indices
            self._graph = Graph(n=self.n)
            self._graph.add_edges(itertools.chain(
                *(list(itertools.combinations(clust[x], 2)) for x in clust)))
            self._update_graph = False
        return self._graph

from abc import ABC, abstractmethod


class LinkageRule(ABC):
    """
    Interface for a linkage rule which can be fitted to data.

    This abstract class specifies three methods. The `fit()` method fits the linkage rule to a pandas DataFrame. The `graph` property can be used after `fit()` to obtain a graph representing the linkage fitted to data.  The `groups` property can be used after `fit()` to obtain a membership vector representing the clustering fitted to data.
    """
    @abstractmethod
    def fit(self, df):
        pass

    @property
    @abstractmethod
    def graph(self):
        pass

    @property
    @abstractmethod
    def groups(self):
        pass

import pandas as pd
from pandas.core.groupby.generic import DataFrameGroupBy

class Data(pd.DataFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def groupby(self, rule):
        super().groupby()

class GroupedData(DataFrameGroupBy):
    pass

l = [[1, 2, 3], [1, None, 4], [2, 1, 3], [1, 2, 2]]
df = pd.DataFrame(l, columns=["a", "b", "c"])
df.groupby
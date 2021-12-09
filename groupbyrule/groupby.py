from pandas import DataFrame
from .groupingrule import GroupingRule


def groupby(df: DataFrame, rule: GroupingRule):
    rule.fit(df)
    return df.groupby(rule.groups)

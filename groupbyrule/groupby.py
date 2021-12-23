from pandas import DataFrame
from .linkagerule import LinkageRule


def groupby(df: DataFrame, rule: LinkageRule):
    rule.fit(df)
    return df.groupby(rule.groups)

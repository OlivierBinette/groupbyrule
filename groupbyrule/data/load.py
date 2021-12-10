from pkg_resources import resource_filename, resource_stream
import pandas as pd


# RL datasets are from https://cran.r-project.org/web/packages/RecordLinkage/index.html


def RLdata500() -> pd.DataFrame:
    RLdata500 = pd.read_csv(
        resource_filename("groupbyrule", "data/RLdata500.csv"),
        index_col=0)
    identity_RLdata500 = pd.read_csv(
        resource_filename("groupbyrule", "data/identity.RLdata500.csv"),
        index_col=0).x

    RLdata500["identity"] = identity_RLdata500

    return RLdata500


def RLdata1000() -> pd.DataFrame:
    RLdata10000 = pd.read_csv(
        resource_filename("groupbyrule", "data/RLdata10000.csv"),
        index_col=0)

    identity_RLdata10000 = pd.read_csv(
        resource_filename("groupbyrule", "data/identity.RLdata10000.csv"),
        index_col=0).x

    RLdata10000["identity"] = identity_RLdata10000

    return RLdata10000


# ABSEmployee dataset is from https://github.com/cleanzr/dblink-experiments


def ABSEmployee() -> pd.DataFrame:
    # dtype = {"RECID": pd.StringDtype(),
    #          "FILEID": pd.StringDtype(),
    #          "ENTID": pd.Int64Dtype(),
    #          "SA1": pd.StringDtype(),
    #          "MB": pd.StringDtype(),
    #          "BDAY": pd.StringDtype(),
    #          "BYEAR": pd.StringDtype(),
    #          "SEX": pd.StringDtype(),
    #          "INDUSTRY": pd.StringDtype(),
    #          "CASUAL": pd.StringDtype(),
    #          "FULLTIME": pd.StringDtype(),
    #          "HOURS": pd.StringDtype(),
    #          "PAYRATE": pd.StringDtype(),
    #          "AWE": pd.StringDtype()}

    ABSEmployee = pd.read_csv(
        resource_stream("groupbyrule", "data/ABSEmployee.csv"), na_values=["."], low_memory=False)
    ABSEmployee.rename({"ENTID": "identity"}, inplace=True)

    return ABSEmployee

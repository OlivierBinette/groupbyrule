from pkg_resources import resource_filename
import pandas as pd

RLdata500 = pd.read_csv(resource_filename("groupbyrule", "data/RLdata500.csv"))
RLdata10000 = pd.read_csv(resource_filename("groupbyrule", "data/RLdata10000.csv"))
identity_RLdata500 = pd.read_csv(resource_filename("groupbyrule", "data/identity.RLdata500.csv"))
identity_RLdata10000 = pd.read_csv(resource_filename("groupbyrule", "data/identity.RLdata10000.csv"))

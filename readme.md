# groupbyrule: group and summarize dataframes using fuzzy and deterministic matching rules

:construction: *under development* :construction:

**groupbyrule** is a Python package for data cleaning and data integration. It provides an extension of [pandas](https://pandas.pydata.org/)' [`groupby`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.groupby.html) function which, instead of grouping rows by a given identifier, groups rows based on logical rules and partial matching. In other words, it provides tools for deterministic record linkage and entity resolution in structured databases. It can also be used for *blocking*, a form of filtering used to speed-up more complex entity resolution algorithms. See the references below to learn more about these topics.

One of the main goal of **groupbyrule** is to be *user-friendly*. Matching rules and clustering algorithms are composable, and the performance of algorithms can be readily evaluted given training data. The package is built on top of [pandas](https://pandas.pydata.org) for data manipulation and on [igraph](https://igraph.org/python/) for graph clustering and related computations.

## Installation

:construction:

## Examples

Consider the `RLdata500` dataset from the [RecordLinkage R package](https://www.google.com/search?channel=fs&client=ubuntu&q=recordlinkage+r+package).

```{python}
from groupbyrule import RLdata500

RLdata500.head()
```

We deduplicate this dataset by linking records which match either on both first name (`fname_c1`) and last name (`lname_c1`), on both first name and birth day (`bd`), or on both last name and birth day. Linkage transitivity is resolved, by default, by considering connected components of the resulting graph.

```{python}
from groupbyrule import Data, Any, Match

Data(RLdata500).groupby(Any(Match(fname_c1", "lname_c1"),
                            Match("fname_c1", "bd"),
                            Match("lname_c1", "bd")))\
               .combine() # Combine the information of matching records in lists 
```

Note that this is not the best way to deduplicate this dataset. However, it showcases the composability of matching rules. The specific rules themselves (exact matching, fuzzy string matching, different clustering algorithms to resolve transitivity) can be customized as needed. A more complete overview is available [here]() :construction:.

A better way to deduplicate this data is to link all pairs of records which agree on all but at most one attribute. This is done below, with the precision and recall computed from the ground truth membership vector `identity_RLdata500`.

```{python}
from groupbyrule import AllButK

Data(RLdata500).groupby(AllButK("fname_c1", "lname_c1", "bd", "bm", "by", k=1))\
               .combine()\
               .precision_recall(identity_RLdata500)
```

### Overview of Linkage Rules

:construction:

### Overview of Clustering Algorithms

:construction:

## References

- Binette, O. & Steorts, R.C. (2021) Almost All of Statistical Entity Resolution. arXiv e-prints, arxiv:
- 
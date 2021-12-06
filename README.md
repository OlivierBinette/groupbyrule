# groupbyrule: deduplicate data using fuzzy and deterministic matching rules

🚧 under construction 🚧

**groupbyrule** is a Python package for data cleaning and data integration. It provides an extension of [pandas](https://pandas.pydata.org/)' [`groupby`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.groupby.html) function which, instead of grouping rows by a given identifier, groups rows based on logical rules and partial matching. In other words, it provides tools for deterministic record linkage and entity resolution in structured databases. It can also be used for *blocking*, a form of filtering used to speed-up more complex entity resolution algorithms. See the references below to learn more about these topics.

One of the main goal of **groupbyrule** is to be *user-friendly*. Matching rules and clustering algorithms are composable, and the performance of algorithms can be readily evaluted given training data. The package is built on top of [pandas](https://pandas.pydata.org) for data manipulation and on [igraph](https://igraph.org/python/) for graph clustering and related computations.

## Installation

🚧

## Examples

Consider the `RLdata500` dataset from the [RecordLinkage R package](https://www.google.com/search?channel=fs&client=ubuntu&q=recordlinkage+r+package).


```python
from groupbyrule import RLdata500

RLdata500.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Unnamed: 0</th>
      <th>fname_c1</th>
      <th>fname_c2</th>
      <th>lname_c1</th>
      <th>lname_c2</th>
      <th>by</th>
      <th>bm</th>
      <th>bd</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>CARSTEN</td>
      <td>NaN</td>
      <td>MEIER</td>
      <td>NaN</td>
      <td>1949</td>
      <td>7</td>
      <td>22</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>GERD</td>
      <td>NaN</td>
      <td>BAUER</td>
      <td>NaN</td>
      <td>1968</td>
      <td>7</td>
      <td>27</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>ROBERT</td>
      <td>NaN</td>
      <td>HARTMANN</td>
      <td>NaN</td>
      <td>1930</td>
      <td>4</td>
      <td>30</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4</td>
      <td>STEFAN</td>
      <td>NaN</td>
      <td>WOLFF</td>
      <td>NaN</td>
      <td>1957</td>
      <td>9</td>
      <td>2</td>
    </tr>
    <tr>
      <th>4</th>
      <td>5</td>
      <td>RALF</td>
      <td>NaN</td>
      <td>KRUEGER</td>
      <td>NaN</td>
      <td>1966</td>
      <td>1</td>
      <td>13</td>
    </tr>
  </tbody>
</table>
</div>



We deduplicate this dataset by linking records which match either on both first name (`fname_c1`) and last name (`lname_c1`), on both first name and birth day (`bd`), or on both last name and birth day. Linkage transitivity is resolved, by default, by considering connected components of the resulting graph.


```python
from groupbyrule import Data, Any, Match

Data(RLdata500).groupby(Any(Match("fname_c1", "lname_c1"),
                            Match("fname_c1", "bd"),
                            Match("lname_c1", "bd")))\
               .combine() # Combine the information of matching records in lists 
```


    ---------------------------------------------------------------------------

    ImportError                               Traceback (most recent call last)

    /tmp/ipykernel_162687/2088331581.py in <module>
    ----> 1 from groupbyrule import Data, Any, Match
          2 
          3 Data(RLdata500).groupby(Any(Match("fname_c1", "lname_c1"),
          4                             Match("fname_c1", "bd"),
          5                             Match("lname_c1", "bd")))\


    ImportError: cannot import name 'Data' from 'groupbyrule' (/home/olivier/Desktop/Research/groupbyrule/groupbyrule/__init__.py)



Note that this is not the best way to deduplicate this dataset. However, it showcases the composability of matching rules. The specific rules themselves (exact matching, fuzzy string matching, different clustering algorithms to resolve transitivity) can be customized as needed. A more complete overview is available [here]() 🚧.

A better way to deduplicate this data is to link all pairs of records which agree on all but at most one attribute. This is done below, with the precision and recall computed from the ground truth membership vector `identity_RLdata500`.


```python
from groupbyrule import AllButK

Data(RLdata500).groupby(AllButK("fname_c1", "lname_c1", "bd", "bm", "by", k=1))\
               .combine()\
               .precision_recall(identity_RLdata500)
```


### Overview of Linkage Rules

🚧

### Overview of Clustering Algorithms

🚧

## References

- Binette, O. & Steorts, R.C. (2021) Almost All of Statistical Entity Resolution. arXiv e-prints, arxiv:
- 

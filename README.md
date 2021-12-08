# groupbyrule: deduplicate data using fuzzy and deterministic matching rules

🚧 under construction 🚧

**groupbyrule** is a Python package for data cleaning and data integration. It integrates with [pandas](https://pandas.pydata.org/)' [`groupby`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.groupby.html) function to, not only group rows by a given identifier, but also groups rows based on logical rules and partial matching. In other words, it provides tools for deterministic record linkage and entity resolution in structured databases. It can also be used for *blocking*, a form of filtering used to speed-up more complex entity resolution algorithms. See the references below to learn more about these topics.

One of the main goal of **groupbyrule** is to be user-friendly. Matching rules and clustering algorithms are composable and the performance of algorithms can be readily evaluted given training data. The package is built on top of [pandas](https://pandas.pydata.org) for data manipulation and on [igraph](https://igraph.org/python/) for graph clustering and related computations.

## Installation

Install from github using the following command:


```sh
pip install git+https://github.com/OlivierBinette/groupbyrule.git
```

## Examples

### Rule-Based Linkage

Consider the `RLdata500` dataset from the [RecordLinkage R package](https://www.google.com/search?channel=fs&client=ubuntu&q=recordlinkage+r+package).


```python
from groupbyrule import RLdata500

RLdata500
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
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
      <th>1</th>
      <td>CARSTEN</td>
      <td>NaN</td>
      <td>MEIER</td>
      <td>NaN</td>
      <td>1949</td>
      <td>7</td>
      <td>22</td>
    </tr>
    <tr>
      <th>2</th>
      <td>GERD</td>
      <td>NaN</td>
      <td>BAUER</td>
      <td>NaN</td>
      <td>1968</td>
      <td>7</td>
      <td>27</td>
    </tr>
    <tr>
      <th>3</th>
      <td>ROBERT</td>
      <td>NaN</td>
      <td>HARTMANN</td>
      <td>NaN</td>
      <td>1930</td>
      <td>4</td>
      <td>30</td>
    </tr>
    <tr>
      <th>4</th>
      <td>STEFAN</td>
      <td>NaN</td>
      <td>WOLFF</td>
      <td>NaN</td>
      <td>1957</td>
      <td>9</td>
      <td>2</td>
    </tr>
    <tr>
      <th>5</th>
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
from groupbyrule import Any, Match, identity_RLdata500, precision_recall
import pandas as pd

# Specify linkage rule
rule = Any(Match("fname_c1", "lname_c1"),
           Match("fname_c1", "bd"),
           Match("lname_c1", "bd"))

# Apply the rule to a dataset
rule.fit(RLdata500)

# Evaluate performance by computing precision and recall
precision_recall(rule.groups, identity_RLdata500)
```




    (0.96, 0.11538461538461539)




Note that this is not the best way to deduplicate this dataset. However, it showcases the composability of matching rules. The specific rules themselves (exact matching, similarity-based string matching, and different clustering algorithms) can be customized as needed. A more complete overview is available [here]() 🚧.

A better way to deduplicate this data is to link all pairs of records which agree on all but at most one attribute. This is done below, with the precision and recall computed from the ground truth membership vector `identity_RLdata500`.


```python
from groupbyrule import AllButK

# Match records matching on all but at most k=1 of the specified attributes
rule = AllButK("fname_c1", "lname_c1", "bd", "bm", "by", k=1)

# Apply the rule to a dataset
rule.fit(RLdata500)

# Evaluate performance by computing precision and recall
precision_recall(rule.groups, identity_RLdata500)
```




    (0.92, 1.0)



### Postprocessing

Following record linkage, records can be processed using pandas's groupby and aggregation functions. Below, we only keep the first non-NA attribute value for each record cluster. This is a simple way to obtain a deduplicated dataset.


```python
RLdata500\
    .groupby(rule.groups)\
    .first()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
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
      <td>CARSTEN</td>
      <td>None</td>
      <td>MEIER</td>
      <td>None</td>
      <td>1949</td>
      <td>7</td>
      <td>22</td>
    </tr>
    <tr>
      <th>1</th>
      <td>GERD</td>
      <td>None</td>
      <td>BAUER</td>
      <td>None</td>
      <td>1968</td>
      <td>7</td>
      <td>27</td>
    </tr>
    <tr>
      <th>2</th>
      <td>ROBERT</td>
      <td>None</td>
      <td>HARTMANN</td>
      <td>None</td>
      <td>1930</td>
      <td>4</td>
      <td>30</td>
    </tr>
    <tr>
      <th>3</th>
      <td>STEFAN</td>
      <td>None</td>
      <td>WOLFF</td>
      <td>None</td>
      <td>1957</td>
      <td>9</td>
      <td>2</td>
    </tr>
    <tr>
      <th>4</th>
      <td>RALF</td>
      <td>None</td>
      <td>KRUEGER</td>
      <td>None</td>
      <td>1966</td>
      <td>1</td>
      <td>13</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>449</th>
      <td>BRITTA</td>
      <td>None</td>
      <td>KOEHLER</td>
      <td>None</td>
      <td>2001</td>
      <td>1</td>
      <td>12</td>
    </tr>
    <tr>
      <th>450</th>
      <td>SABINE</td>
      <td>None</td>
      <td>SCHNEIDER</td>
      <td>None</td>
      <td>1953</td>
      <td>5</td>
      <td>20</td>
    </tr>
    <tr>
      <th>451</th>
      <td>MARIA</td>
      <td>None</td>
      <td>SCHNEIDER</td>
      <td>None</td>
      <td>1981</td>
      <td>8</td>
      <td>8</td>
    </tr>
    <tr>
      <th>452</th>
      <td>INGE</td>
      <td>None</td>
      <td>SCHREIBER</td>
      <td>None</td>
      <td>1967</td>
      <td>12</td>
      <td>13</td>
    </tr>
    <tr>
      <th>453</th>
      <td>KARIN</td>
      <td>None</td>
      <td>GUENTHER</td>
      <td>None</td>
      <td>1941</td>
      <td>8</td>
      <td>19</td>
    </tr>
  </tbody>
</table>
<p>454 rows × 7 columns</p>
</div>




### Similarity-Based Linkage Rules

🚧

### Supervised Approaches and Learning Rules

🚧

### Clustering Algorithms

🚧

### Performance Evaluation

🚧

## References

🚧


[![test](https://github.com/OlivierBinette/groupbyrule/actions/workflows/python-package-conda.yml/badge.svg)](https://github.com/OlivierBinette/groupbyrule/actions/workflows/python-package-conda.yml) 

# :link: GroupByRule: deduplicate data using fuzzy and deterministic matching rules

🚧 under construction 🚧

**GroupByRule** is a Python package for data cleaning and deduplication. It integrates with [pandas](https://pandas.pydata.org/)' [`groupby`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.groupby.html) function to not only group dataframe rows by a given identifier, but also groups rows based on logical rules and partial matching. In other words, it provides tools for deterministic record linkage and entity resolution in structured databases. It can also be used for *blocking*, a form of filtering used to speed-up more complex entity resolution algorithms. See the references below to learn more about these topics.

One of the main goal of **GroupByRule** is to be user-friendly. Matching rules and clustering algorithms are composable and the performance of algorithms can be readily evaluated given training data. The package is built on top of [pandas](https://pandas.pydata.org) for data manipulation and on [igraph](https://igraph.org/python/) for graph clustering and related computations.

Additionally, **GroupByRule** contains the `comparator` submodule which provides efficient C++ implementations of common [string distance functions](https://en.wikipedia.org/wiki/String_metric). This can be of independent interest as well.

## Installation

Install from github using the following command:

     pip install git+https://github.com/OlivierBinette/groupbyrule.git

## Examples

### Rule-Based Linkage

Consider the `RLdata500` dataset from the [RecordLinkage R package](https://www.google.com/search?channel=fs&client=ubuntu&q=recordlinkage+r+package).


```python
from groupbyrule.data import load_RLdata500

df = load_RLdata500()
df.head()
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
      <th>identity</th>
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
      <td>34</td>
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
      <td>51</td>
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
      <td>115</td>
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
      <td>189</td>
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
      <td>72</td>
    </tr>
  </tbody>
</table>
</div>



We deduplicate this dataset by linking records which match either on both first name (`fname_c1`) and last name (`lname_c1`), on both first name and birth day (`bd`), or on both last name and birth day. Linkage transitivity is resolved, by default, by considering connected components of the resulting graph. Precision and recall are computed from the ground truth membership vector `identity_RLdata500`.


```python
from groupbyrule import Any, Match, precision_recall

# Specify linkage rule
rule = Any(Match("fname_c1", "lname_c1"),
           Match("fname_c1", "bd"),
           Match("lname_c1", "bd"))

# Apply the rule to a dataset
rule.fit(df)

# Evaluate performance by computing precision and recall
precision_recall(rule.groups, df.identity)
```




    (0.11538461538461539, 0.96)




This is not the best way to deduplicate this dataset, but the above showcases the composability of matching rules. The specific rules themselves (exact matching, similarity-based string matching, and different clustering algorithms) can be customized as needed. A more complete overview is available [here]() 🚧.

A better way to deduplicate this data is to link all pairs of records which agree on all but at most one attribute. This is done below.


```python
from groupbyrule import AllButK

# Link records agreeing on all but at most k=1 of the specified attributes
rule = AllButK("fname_c1", "lname_c1", "bd", "bm", "by", k=1)

# Apply the rule to a dataset
rule.fit(df)

# Evaluate performance by computing precision and recall
precision_recall(rule.groups, df.identity)
```




    (1.0, 0.92)



#### Postprocessing

Following record linkage, records can be processed using pandas's groupby and aggregation functions. Below, we only keep the first non-NA attribute value for each record cluster. This is a simple way to obtain a deduplicated dataset.


```python
deduplicated = df.groupby(rule.groups).first()
```

### String Distance Functions

**GroupByRule** provides a suite of string and numerical similarity functions as part of its `comparator` submodule. String similarity functions include the Levenshtein distance, 🚧, and 🚧. These similarity functions can be used on their own as shown below, or for the definition of linkage rules as explained in the following section. This is heavily inspired by Neil Marchant's excellent [Comparator](https://github.com/ngmarchant/comparator) R package, but not quite equivalent in its scope and implementation.

String distance functions are implemented through subclasses of the `Comparator` abstract base case. `Comparator` objects are used to instanciate comparison functions while allowing data in memory to be recycled across function calls. The `compare()` method can then be used to compare elements, the `pairwise()` method can be used to compare all pairs of elements between two lists, and the `elementwise()` method can be used to compare corresponding elements.

Below are examples of the comparison functions currently provided. These are implemented in C++ for efficiency.

#### Levenshtein Distance


```python
from groupbyrule.comparator import Levenshtein

cmp = Levenshtein(normalize=True)
cmp.compare("Olivier", "Oliver")  
```




    0.14285714285714285




```python
cmp.elementwise(["Olivier", "Oliver", "Olivia"], 3*["Olivier"])
```




    [0.0, 0.14285714285714285, 0.26666666666666666]




```python
cmp.pairwise(["Olivier", "Oliver", "Olivia"], ["Olivier", "test", "Other"])
```




    [[0.0, 0.7777777777777778, 0.5],
     [0.14285714285714285, 0.75, 0.42857142857142855],
     [0.26666666666666666, 0.75, 0.625]]



#### Longest Common Subsequence (LCS) Distance


```python
from groupbyrule.comparator import LCSDistance

cmp = LCSDistance(normalize=True)
cmp.compare("Olivier", "Oliver")
```




    0.14285714285714285




### Similarity-Based Linkage Rules

🚧

### Supervised Approaches and Learning Rules

🚧

### Clustering Algorithms

🚧

### Performance Evaluation

🚧

### Privacy-Preserving Record Linkage

🚧

#### Cryptographic Primitives

🚧

#### Multiparty Computation Protocols

🚧


## References

🚧



```python

```

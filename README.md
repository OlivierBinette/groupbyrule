# GroupByRule: deduplicate data using fuzzy and deterministic matching rules

🚧 under construction 🚧

**GroupByRule** is a Python package for data cleaning and deduplication. It integrates with [pandas](https://pandas.pydata.org/)' [`groupby`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.groupby.html) function to not only group dataframe rows by a given identifier, but also groups rows based on logical rules and partial matching. In other words, it provides tools for deterministic record linkage and entity resolution in structured databases. It can also be used for *blocking*, a form of filtering used to speed-up more complex entity resolution algorithms. See the references below to learn more about these topics.

One of the main goal of **GroupByRule** is to be user-friendly. Matching rules and clustering algorithms are composable and the performance of algorithms can be readily evaluated given training data. The package is built on top of [pandas](https://pandas.pydata.org) for data manipulation and on [igraph](https://igraph.org/python/) for graph clustering and related computations.

## Installation

Install from github using the following command:

     pip install git+https://github.com/OlivierBinette/groupbyrule.git

## Examples

### Rule-Based Linkage

Consider the `RLdata500` dataset from the [RecordLinkage R package](https://www.google.com/search?channel=fs&client=ubuntu&q=recordlinkage+r+package).


```python
from groupbyrule.data import load_RLdata500

df = load_RLdata500()
df
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
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>496</th>
      <td>GABRIHELE</td>
      <td>NaN</td>
      <td>BECKER</td>
      <td>NaN</td>
      <td>1990</td>
      <td>3</td>
      <td>27</td>
      <td>413</td>
    </tr>
    <tr>
      <th>497</th>
      <td>SABINE</td>
      <td>NaN</td>
      <td>SCHNEIDER</td>
      <td>NaN</td>
      <td>1953</td>
      <td>5</td>
      <td>20</td>
      <td>378</td>
    </tr>
    <tr>
      <th>498</th>
      <td>MARIA</td>
      <td>NaN</td>
      <td>SCHNEIDER</td>
      <td>NaN</td>
      <td>1981</td>
      <td>8</td>
      <td>8</td>
      <td>399</td>
    </tr>
    <tr>
      <th>499</th>
      <td>INGE</td>
      <td>NaN</td>
      <td>SCHREIBER</td>
      <td>NaN</td>
      <td>1967</td>
      <td>12</td>
      <td>13</td>
      <td>315</td>
    </tr>
    <tr>
      <th>500</th>
      <td>KARIN</td>
      <td>NaN</td>
      <td>GUENTHER</td>
      <td>NaN</td>
      <td>1941</td>
      <td>8</td>
      <td>19</td>
      <td>238</td>
    </tr>
  </tbody>
</table>
<p>500 rows × 8 columns</p>
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



### Postprocessing

Following record linkage, records can be processed using pandas's groupby and aggregation functions. Below, we only keep the first non-NA attribute value for each record cluster. This is a simple way to obtain a deduplicated dataset.


```python
df.groupby(rule.groups).first()
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
      <th>0</th>
      <td>CARSTEN</td>
      <td>None</td>
      <td>MEIER</td>
      <td>None</td>
      <td>1949</td>
      <td>7</td>
      <td>22</td>
      <td>34</td>
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
      <td>51</td>
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
      <td>115</td>
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
      <td>189</td>
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
      <td>72</td>
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
      <td>424</td>
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
      <td>378</td>
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
      <td>399</td>
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
      <td>315</td>
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
      <td>238</td>
    </tr>
  </tbody>
</table>
<p>454 rows × 8 columns</p>
</div>




```python
from groupbyrule.data import load_ABSEmployee

df = load_ABSEmployee()

df
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
      <th>RECID</th>
      <th>FILEID</th>
      <th>ENTID</th>
      <th>SA1</th>
      <th>MB</th>
      <th>BDAY</th>
      <th>BYEAR</th>
      <th>SEX</th>
      <th>INDUSTRY</th>
      <th>CASUAL</th>
      <th>FULLTIME</th>
      <th>HOURS</th>
      <th>PAYRATE</th>
      <th>AWE</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>A000001</td>
      <td>A</td>
      <td>1</td>
      <td>10929</td>
      <td>1092903.0</td>
      <td>168.0</td>
      <td>1954</td>
      <td>2</td>
      <td>4.0</td>
      <td>0</td>
      <td>0</td>
      <td>17</td>
      <td>35.00</td>
      <td>595.00</td>
    </tr>
    <tr>
      <th>1</th>
      <td>A000002</td>
      <td>A</td>
      <td>2</td>
      <td>10981</td>
      <td>1098109.0</td>
      <td>26.0</td>
      <td>1998</td>
      <td>1</td>
      <td>1.0</td>
      <td>0</td>
      <td>1</td>
      <td>40</td>
      <td>40.00</td>
      <td>1600.00</td>
    </tr>
    <tr>
      <th>2</th>
      <td>A000006</td>
      <td>A</td>
      <td>6</td>
      <td>10768</td>
      <td>1076809.0</td>
      <td>168.0</td>
      <td>1990</td>
      <td>2</td>
      <td>2.0</td>
      <td>0</td>
      <td>1</td>
      <td>40</td>
      <td>43.20</td>
      <td>1728.00</td>
    </tr>
    <tr>
      <th>3</th>
      <td>A000009</td>
      <td>A</td>
      <td>9</td>
      <td>10399</td>
      <td>1039905.0</td>
      <td>344.0</td>
      <td>1997</td>
      <td>1</td>
      <td>1.0</td>
      <td>0</td>
      <td>1</td>
      <td>42</td>
      <td>41.00</td>
      <td>1722.00</td>
    </tr>
    <tr>
      <th>4</th>
      <td>A000012</td>
      <td>A</td>
      <td>12</td>
      <td>10616</td>
      <td>1061607.0</td>
      <td>190.0</td>
      <td>1954</td>
      <td>2</td>
      <td>2.0</td>
      <td>0</td>
      <td>1</td>
      <td>40</td>
      <td>45.00</td>
      <td>1800.00</td>
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
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>659995</th>
      <td>C399994</td>
      <td>C</td>
      <td>399994</td>
      <td>10381</td>
      <td>1038105.0</td>
      <td>30.0</td>
      <td>1964</td>
      <td>2</td>
      <td>5.0</td>
      <td>0</td>
      <td>0</td>
      <td>16</td>
      <td>37.10</td>
      <td>593.60</td>
    </tr>
    <tr>
      <th>659996</th>
      <td>C399996</td>
      <td>C</td>
      <td>399996</td>
      <td>10508</td>
      <td>1050807.0</td>
      <td>150.0</td>
      <td>1992</td>
      <td>1</td>
      <td>1.0</td>
      <td>0</td>
      <td>1</td>
      <td>41</td>
      <td>46.50</td>
      <td>1906.50</td>
    </tr>
    <tr>
      <th>659997</th>
      <td>C399997</td>
      <td>C</td>
      <td>399997</td>
      <td>10969</td>
      <td>1096907.0</td>
      <td>78.0</td>
      <td>1988</td>
      <td>2</td>
      <td>3.0</td>
      <td>1</td>
      <td>0</td>
      <td>18</td>
      <td>47.52</td>
      <td>855.36</td>
    </tr>
    <tr>
      <th>659998</th>
      <td>C399998</td>
      <td>C</td>
      <td>399998</td>
      <td>10096</td>
      <td>1009601.0</td>
      <td>67.0</td>
      <td>1968</td>
      <td>1</td>
      <td>5.0</td>
      <td>1</td>
      <td>0</td>
      <td>6</td>
      <td>44.94</td>
      <td>269.64</td>
    </tr>
    <tr>
      <th>659999</th>
      <td>C400000</td>
      <td>C</td>
      <td>400000</td>
      <td>10126</td>
      <td>1012607.0</td>
      <td>123.0</td>
      <td>1967</td>
      <td>1</td>
      <td>5.0</td>
      <td>0</td>
      <td>0</td>
      <td>19</td>
      <td>37.45</td>
      <td>711.55</td>
    </tr>
  </tbody>
</table>
<p>660000 rows × 14 columns</p>
</div>




```python
rule = AllButK("BDAY", "BYEAR", "SEX", "INDUSTRY", "CASUAL", "FULLTIME", "SA1", "MB", k=1)

rule.fit(df)
rule.groups
```




    array([     0,      1,      2, ..., 414020, 414021, 414022])




```python
import pandas as pd
import numpy as np
from scipy.special import comb

precision_recall(rule.groups, df.ENTID)
```




    (0.8003150813727027, 0.9226032258064516)




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


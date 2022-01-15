.. GroupByRule documentation master file, created by
   sphinx-quickstart on Thu Jan 13 08:30:41 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

GroupByRule
===========

Deduplicate data using fuzzy and deterministic matching rules.

.. toctree::
   :maxdepth: 2
   :caption: API Documentation:

   source/groupbyrule


🚧 under construction 🚧

**GroupByRule** is a Python package for data cleaning and deduplication. It integrates with `pandas <https://pandas.pydata.org/>`_' `groupby() <https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.groupby.html>`_ function to not only group dataframe rows by a given identifier, but also groups rows based on logical rules and partial matching. In other words, it provides tools for deterministic record linkage and entity resolution in structured databases. It can also be used for *blocking*, a form of filtering used to speed-up more complex entity resolution algorithms. See the references below to learn more about these topics.

One of the main goal of **GroupByRule** is to be user-friendly. Matching rules and clustering algorithms are composable and the performance of algorithms can be readily evaluated given training data. The package is built on top of `pandas <https://pandas.pydata.org/>`_ for data manipulation and on `igraph <https://igraph.org/python/>`_ for graph clustering and related computations.

Additionally, **GroupByRule** provides highly efficient C++ implementations of common `string distance functions <https://en.wikipedia.org/wiki/String_metric>`_ through its ``comparator`` submodule. This can be used independently of record linkage algorithms.


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

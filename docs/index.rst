RockyDB
===================================
A NoSQL database written in Python. It 
utilises rocksdb as a storage engine. 

.. toctree::
   :caption: Contents:
   :hidden:
   :maxdepth: 4
   :titlesonly:

   self
   usage
 

.. toctree::
   :caption: Development:
   :hidden:

   changelog
   Github <https://github.com/aaldulimi/RockyDB>
   

Features 
------------
Currently under active development, however here is the feature list so far:

- **Create collections**
- **Insert, get and delete documents**
- **REST API**
- **Query language**
- **Indexes**

Installation
------------

.. code::

   pip install rockydb


Perfomance
--------------
Dataset: `NBA Players Dataset <https://www.kaggle.com/datasets/drgilermo/nba-players-stats>`_
Computer: MacBook Pro (13-inch, 2019).
RockyDB is still in its early days, these results will likely get better in the future. 

.. list-table:: 
   :widths: 25 25 25 25 25
   :align: left
   :header-rows: 1

   * - Database
     - Insert
     - Get 
     - Query
     - Delete
   * - RockyDB
     - **0.00074**
     - **0.00038**
     - 0.00014
     - **0.00023**
   * - MongoDB
     - 0.04436
     - 0.04518
     - **0.00004**
     - 0.04264
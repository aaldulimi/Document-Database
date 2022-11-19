# RockyDB 
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
![CI](https://github.com/aaldulimi/rockydb/actions/workflows/integrate.yml/badge.svg)
[![codecov](https://codecov.io/github/aaldulimi/RockyDB/branch/master/graph/badge.svg?token=6MZLCKX5IJ)](https://codecov.io/github/aaldulimi/RockyDB)

Simple NoSQL database written in Python. It relies on rocksdb as its storage engine. This is more of a Proof-of-concept than a production-ready database. 

## Installation 
```
pip install rockydb
```

## Contents
- [RockyDB](#rockydb)
- [Installation](#installation)
- [Contents](#contents)
- [Features](#features)
- [Documentation](#documentation)
    - [Create collection](#create-collection)
    - [Insert doucment](#insert-document)
    - [Get document](#get-document)
    - [Delete document](#delete-document)
    - [Query](#query)
    


## Features
Currently under active development, however here is the feature list so far:

- **Create collections**
- **Insert, get and delete documents**
- **REST API**
- **Query language**
- **Indexes**
- **Full-text Search [IN-DEVELOPMENT]**

## Performance
Dataset: [NBA Players Dataset](https://www.kaggle.com/datasets/drgilermo/nba-players-stats).
Computer: MacBook Pro (13-inch, 2019).
RockyDB is still in its early days, these results will likely get better in the future. 
| Database      | Insert | Get | Query | Delete 
| -----------| -----------:| -----------:| -----------:| -----------:| 
| RockyDB      | **0.00074**       | **0.00038** | 0.00014 | **0.00023**
| MongoDB   | 0.04436        | 0.04518 | **0.00004**  | 0.04264

## Documentation
Full [Documentation](https://rockydb.readthedocs.io/en/latest/). Below are the basics:
### Create collection 
```python
from rockydb import RockyDB

db = RockyDB(path="database/")
news = db.collection("news")
```

### Insert document
Supported data types: `str`, `int`, `float`, `bool` and `list`. Will support more later. 
```python
doc_id = news.insert({
  "title": "Can store strings",
  "year": 2022,
  "people": ["lists", "are", "fine", "too"],
  "pi": 3.14,
  "real": True
})
```
The `insert` method will return a unique document `_id`. `_id` will be created if document does not contain it.  

### Get document
```python
news.get(doc_id)
```
### Delete document
```python
news.delete(doc_id)
```
### Query
```python
news.find({"pi?lt": 3.14, "real": True}, limit=10)
``` 
The `limit` arg is optional, default is 10. Supports exact, lte, lt, gt and gte queries.

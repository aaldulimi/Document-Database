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
- **Full-text Search [IN-DEVELOPMENT]**

## Performance
This benchmark is based on the [NBA Players Dataset](https://www.kaggle.com/datasets/drgilermo/nba-players-stats) which contains 3921 rows (unique documents).
| Database      | Insertion |
| ----------- | ----------- |
| RockyDB      | 0.67       |
| MongoDB   | 1.62        |

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
  "title": "Elon Musk Completes $44 Billion Deal to Own Twitter",
  "year": 2022,
  "people": ["Elon Musk"],
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

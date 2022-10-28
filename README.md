# PaperDB 
Simple document (i.e. NoSQL) database written in Python. This is more of a Proof-of-concept than a production-ready database. 

## Contents
- [PaperDB](#paperdb)
  - [Contents](#contents)
  - [Features](#features)
  - [Installation](#installation)
  - [Usage](#usage)
    - [Create collection](#create-collection)
    - [Insert doucment](#insert-document)
    - [Get document](#get-document)
    - [Query](#query)
    - [Full-text search](#full-text-search)
    


## Features
Currently under active development, however here are some things that you can do

- **Insert document(s)**
- **Exact and contains search**
- **Delete document(s)**
- **REST API**
- **Full-text search**
- [IN-DEVELOPMENT] Documentation
- [SOON] Support lt, gt, lte, gte, contains and range queries
- [SOON] Benchmarks 
- [SOON] Indexes 
- [SOON] Tensor search


## Installation 
Git clone this repo, cd into the root directory and run ```poetry install```. This does require [poetry](https://python-poetry.org/) to be installed on your local machine. 

## Usage
Full documentation will come later. For now, here are the basics:
### Create collection 
```python
from src.paper import PaperDB

db = PaperDB(path="database/")
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
The `insert` method will return a unique document `_id` 

### Get document
```python
news.get(doc_id)
```

### Query
```python
news.find({"pi": 3.14, "real": True}, limit=10)
``` 
The `limit` arg is optional.
### Full-text search 
```python
index = news.create_index("title_index", fields=["title"])
index.search("some query here", fields=["title"], limit=10)
```
The `fields` and `limit` args are both optional

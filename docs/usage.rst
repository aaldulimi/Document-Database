Usage
========

Instantiating 
----------------
.. code::

    from rockydb import RockyDB

    db = RockyDB('database/')
    posts = db.collection("posts") 


Inserting documents 
------------------------
.. code::

    doc_id = posts.insert({
        "title": "Something goes here",
        "age": 47,
        "real": True,
        "arr": [1, 2, 3]
        })

Getting documents 
----------------------
.. code::

    doc = posts.get(doc_id)

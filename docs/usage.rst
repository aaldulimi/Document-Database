Usage
=========

Instantiate Collection
--------------------------

Create a collection to store the documents (equivalent to a table in SQL)

.. code:: python

    from rockydb import RockyDB

    db = RockyDB('database/') # specify the path to store the database
    posts = db.collection("posts") # creating a collection named "posts"


Basic Usage
-----------------

Insert
^^^^^^^^^
Store a document in the database 

.. code:: python

    insert(doc: dict)

**Parameters**

**doc** (required) - ``dict``

If there is no ``_id`` field in the document, an ``_id`` will be randomly generated.
The document supports the following data-types: ``int``, ``str``, ``float``, ``bool`` and ``list``.

Example

.. code:: python

    doc_id = posts.insert({
        "title": "A Housing Crisis Has More Politicians Saying Yes to Big Real Estate",
        "author": "Mihir Zaveri",
        "year": 2022,
        "source": "https://www.nytimes.com/2022/10/16/nyregion/politicians-housing-crisis-real-estate.html",
    })

**Returns** the ``_id`` of the document



Get
^^^^^^^^^
Retrieves a document from the database using its ``_id``.

.. code:: python

    get(id: str)

**Parameters**

**id** (required) - ``str``

Example 

.. code:: python

    doc = posts.get("DBDV73BQ")

**Returns** the ``document`` if it exists, otherwise will return ``None``.



Delete
^^^^^^^^^
Deletes a document from the database using its ``_id`` .

.. code:: python

    delete(id: str)

**Parameters**

**id** (required) - ``str``

Example 

.. code:: python

    posts.delete("DBDV73BQ")

**Returns** ``True`` if document was found and deleted, otherwise will return ``False``.


Find
^^^^^^^^^
Returns documents that match a query

.. code:: python

    find(query: dict, limit: int = 10)

**Parameters**

**query** (required) - ``dict``
    - The query ``key`` corresponds to the document ``key`` and the query ``value`` corresponds to its ``value`` in the document.

**limit** (optional) - ``int``, default is ``10``

Example

.. code:: python

    docs = posts.query({"title": "some value", "year": 2022})

The above query translates to ``("title" == "some value") AND ("year" == 2022)``. There is currently no support
for ``OR`` type queries. Its currently being implemented.

Can also search for ``lt (less-than)``, ``lte (less-than equals)``, ``gt (greater-than)`` and gte ``(greater-than equals)``.
To do so, place a ``?`` after the ``key`` in the query, and type ``lt`` or any of the other options.

Example 

.. code:: python

    docs = posts.query({"year?lte": 2050})

**Returns** a ``list`` containing all the ``documents`` found. ``list`` will 
be empty if no documents matched the query.


Indexes
-----------------
Create an index on a specific document field to speed up queries

Create
^^^^^^^^^
Create the index 

.. code:: python

    create_index(name: str, field: str)

**Parameters**

**name** (required) - ``str``

**field** (required) - ``str``

Example 

.. code:: python

    posts.create_index("age_index", "age")

**Returns** an ``Index`` object if creation was successful. Otherwise will return ``None``.


Find
^^^^^^^^^
Query the index

.. code:: python

    find(query: dict, field: str)

**Parameters**

**name** (required) - ``str``

**field** (required) - ``str``

Example 

.. code:: python

    posts.create_index("age_index", "age")

**Returns** an ``Index`` object if creation was successful. Otherwise will return ``None``.

..  
    Text Search
    ^^^^^^^^^^^^^^^^^
    Implement full-text search on all documents. This is a 2-step process. You must first 
    create an index, and then use that index to lookup documents.

    Create Index 
    #################

    .. code:: python

        index = posts.create_index(name: str, fields: list)


    **Parameters**

    **name** (required) - ``str``

    **fields** (required) - ``list``, the text fields of each document to index

    Example 

    .. code:: python

        index = posts.create_index(name="title_index", fields=["title", "author"])

    **Returns** an ``Index`` object if the index has been successfully created. This line of code 
    might take some time to run depending on the size of the database, as it needs to go through 
    all documents.


    Use Index 
    #################

    .. code:: python

        index.search(query: str, fields: list = None, limit: int = 10)

    **Parameters**

    **query** (required) - ``str``

    **fields** (optional) - ``list``
        - a subset (or all) of the fields used when creating the index. Will use the same fields 
        as the ones specified when creating the index.

    **limit** (optional): ``int``, default is ``10``


    Example 

    .. code:: python

        docs = index.search("Housing", fields=["title"], limit=1)

    **Returns** a ``list`` containing all the ``documents`` found. ``list`` will 
    be empty if no documents matched the query.
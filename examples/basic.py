import sys
sys.path.append('/Users/flyinshark/Desktop/RockyDB/')
from rockydb import RockyDB

# connect to db
db = RockyDB("database/")

# create a collection
articles = db.collection("articles")

# insert a document (_id will be generated if its not included in the document)
# will return the _id of the document
doc_id = articles.insert(
    {
        "title": "A Housing Crisis Has More Politicians Saying Yes to Big Real Estate",
        "author": "Mihir Zaveri",
        "source": "https://www.nytimes.com/2022/10/16/nyregion/politicians-housing-crisis-real-estate.html",
    }
)

# can also insert multiple documents, documents aren't bound to a specific schema
articles.insert_batch(
    [
        {
            "title": "How Russian Action Movies Are Selling War",
            "body": "Mihir Zaveri",
        },
        {
            "title": "Apple Store in Oklahoma City Becomes Second to Unionize",
            "number": 5,
        },
    ]
)

# get entire document using its id
document = articles.get(doc_id)

# delete a document using its id
articles.delete(doc_id)

# query documents
query = articles.find({"author": "Mihir Zaveri", "number": 5})

# create an index
number_index = articles.create_index(name="number_index", field="number")

# query index 
index_query = number_index.find({"number?lte": 10})

# print results
print(query)
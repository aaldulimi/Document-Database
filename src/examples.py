from database import DocDB


# connect to db 
db = DocDB("../database/")

# create a collection
posts = db.collection("posts")


# insert a document (_id will be generated if its not included in the document)
# will return the _id of the document 
doc_id = db.insert({
        "title": "A Housing Crisis Has More Politicians Saying Yes to Big Real Estate",
        "author": "Mihir Zaveri",
        "source": "https://www.nytimes.com/2022/10/16/nyregion/politicians-housing-crisis-real-estate.html"
        })

# can also insert multiple documents, documents aren't bound to a specific schema
doc_id = db.insert_batch([{
        "title": "How Russian Action Movies Are Selling War",
        "body": "Mihir Zaveri",
    }, {
        "title": "Apple Store in Oklahoma City Becomes Second to Unionize"
    }])

# get entire document using its id 
document = db.get(doc_id)

# delete a document using its id
db.delete(doc_id)

# can perform exact or contains type searches on any document field 
exact_result = db.search(field="author", value="Julie Turkewitz", type="exact")
contains_result = db.search(field="author", value="J", type="contains", max_count=1)

# can create a full-text search index, specifying which fields to index
index = db.create_full_text_index("index_name", fields=["title"])

# you can also use a old index that you created in an older session 
index = db.get_index("index_name")

# once you have an index, can now use to perform full-text search on a subset (or all)
# of the fields you indexed
text_search = db.text_search(index, query="Global Fallout", fields=["title"], count=2)





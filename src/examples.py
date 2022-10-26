from docdb import DocDB

# connect to db 
db = DocDB("database/")

# create a collection
news = db.collection("posts")

# insert a document (_id will be generated if its not included in the document)
# will return the _id of the document 
doc_id = news.insert({
        "title": "A Housing Crisis Has More Politicians Saying Yes to Big Real Estate",
        "author": "Mihir Zaveri",
        "source": "https://www.nytimes.com/2022/10/16/nyregion/politicians-housing-crisis-real-estate.html"
        })

# can also insert multiple documents, documents aren't bound to a specific schema
news.insert_batch([{
        "title": "How Russian Action Movies Are Selling War",
        "body": "Mihir Zaveri",
    }, {
        "title": "Apple Store in Oklahoma City Becomes Second to Unionize"
    }])

# get entire document using its id 
document = news.get(doc_id)

# delete a document using its id
news.delete(doc_id)

# can perform exact or contains type searches on any document field 
exact_result = news.search(field="author", value="Julie Turkewitz", type="exact")
contains_result = news.search(field="author", value="J", type="contains", max_count=1)

# can create a full-text search index, specifying which fields to index
index = news.create_index("title_index", fields=["title"])

# you can also use a old index that you created in an older session, this index will not be recreated 
index = news.use_index("title_index")

# once you have an index, can now use to perform full-text search on a subset (or all)
# of the fields you indexed
text_search = news.text_search(index, query="Global Fallout", fields=["title"], count=2)

# print results
print(text_search)





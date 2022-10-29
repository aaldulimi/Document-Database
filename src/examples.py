from paper import PaperDB

# connect to db
db = PaperDB("database/")

# create a collection
news = db.collection("yolo")

# insert a document (_id will be generated if its not included in the document)
# will return the _id of the document
doc_id = news.insert(
    {
        "title": "A Housing Crisis Has More Politicians Saying Yes to Big Real Estate",
        "author": "Mihir Zaveri",
        "source": "https://www.nytimes.com/2022/10/16/nyregion/politicians-housing-crisis-real-estate.html",
    }
)

# can also insert multiple documents, documents aren't bound to a specific schema
# news.insert_batch([{
#         "title": "How Russian Action Movies Are Selling War",
#         "body": "Mihir Zaveri",
#     }, {
#         "title": "Apple Store in Oklahoma City Becomes Second to Unionize",
#         "number": 5,
#     }])

# # get entire document using its id
# document = news.get(doc_id)

# # delete a document using its id
# news.delete(doc_id)

# # can create a full-text search index, specifying which fields to index
# index = news.create_index("title_index", fields=["title"])

# # you can also use a old index that you created in an older session, this index will not be recreated
# index = news.get_index("title_index")

# # once you have an index, can now use to perform full-text search on a subset (or all)
# # of the fields you indexed
# text_search = index.search(query="Russian", fields=["title"], limit=1)

# # new query method (in-development)
# query = news.find({"author": "Mihir Zaveri", "number": 5})

# # print results
# print(text_search)
print(news.get("Qy2hS9Rl"))
news.delete("Qy2hS9Rl")

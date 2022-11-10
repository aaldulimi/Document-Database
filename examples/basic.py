import sys
sys.path.append('/Users/flyinshark/Desktop/RockyDB/')
from rockydb import RockyDB
import time
import pandas as pd
import threading

# connect to db
db = RockyDB("database2/")

# create a collection
articles = db.collection("articles")

# df = pd.read_csv('examples/Players.csv')
# df = df.rename(columns={'id': '_id'})

# df = df.astype({"_id": str})

# # =========================
# players = df.to_dict(orient='records')


# start = time.time()

# for player in players:
#     del player["_id"]
#     articles.insert(player)

# # articles.insert_batch(players)

# end = time.time()

# print("total time:", end - start)
# insert a document (_id will be generated if its not included in the document)
# will return the _id of the document
# doc_id = articles.insert(
#     {
#         "title": "A Housing Crisis Has More Politicians Saying Yes to Big Real Estate",
#         "author": "Mihir Zaveri",
#         "source": "https://www.nytimes.com/2022/10/16/nyregion/politicians-housing-crisis-real-estate.html",
#     }
# )

# # can also insert multiple documents, documents aren't bound to a specific schema
# articles.insert_batch(
#     [
#         {
#             "title": "How Russian Action Movies Are Selling War",
#             "body": "Mihir Zaveri",
#         },
#         {
#             "title": "Apple Store in Oklahoma City Becomes Second to Unionize",
#             "number": 5,
#         },
#     ]
# )

# # get entire document using its id
# document = articles.get(doc_id)

# # delete a document using its id
# articles.delete(doc_id)



start = time.time()
# thread.start()
# thread.join()
query = articles.find({"height?gt": 178})
end = time.time()

# # print results
print("total time:", end - start)


# .003 without parrallelism 

from writer import DocumentDB
from document import Document



db = DocumentDB()

doc = Document("sample title", "this is the body of the document")
db.insert(doc)

print(db.get("title"))





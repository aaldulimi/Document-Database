from document_db import DocumentDB
from document import Document

if __name__ == "__main__":
    db = DocumentDB()

    doc_1 = Document("Global Fallout From Rate Moves Won’t Stop the Fed",
        "Jeanna Smialek and Alan Rappeport", "The Federal Reserve, like many central banks...")

    doc_2 = Document("In Record Numbers, Venezuelans Risk a Deadly Trek to Reach the U.S. Border",
        "Julie Turkewitz", "Two crises are converging at the perilous land bridge known as the Darién Gap...")

    db.insert_object(doc_1)
    db.insert_object(doc_2)


    doc_3 = {
        "title": "Another document",
        "author": "Some author",
        "body": "The content of the document",
        "random": "a new field that no other document has"
    }

    db.insert(doc_3)


    
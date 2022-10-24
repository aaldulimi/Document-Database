from src.database import DocDB
from src.document import Document

class TestInsertions:
    def test_one_document(self):
        db = DocDB("database/")

        doc = {
            "title": "Another document",
            "author": "Some author with a J",
            "body": "The content of the document"
        }
        
        doc_id = db.insert(doc)
        get_doc = db.get(doc_id)

        assert doc == get_doc

    def test_batch_documents(self):
        db = DocDB("database/")

        doc_1 = {
            "_id": "doc1",
            "title": "Document 2",
            "author": "Tim",
            "body": "This is for the batch test"
        }

        doc_2 = {
            "_id": "doc2",
            "author": "Smith",
            "body": "Another filler document"
        }

        docs = [doc_1, doc_2]
        db.insert_batch(docs)

        get_doc_1 = db.get("doc1")
        get_doc_2 = db.get("doc2")

        assert doc_1 == get_doc_1
        assert doc_2 == get_doc_2


    def test_one_object(self):
        db = DocDB("database/")

        doc = Document("In Record Numbers, Venezuelans Risk a Deadly Trek to Reach the U.S. Border",
            "Julie Turkewitz", "Two crises are converging at the perilous land bridge known as the Darién Gap...")

        doc_id = db.insert_object(doc)
        get_doc = db.get(doc_id)

        del get_doc["_id"]

        assert doc.__dict__ == get_doc

    def test_batch_objects(self):
        db = DocDB("database/")

        doc_1 = Document("In Record Numbers, Venezuelans Risk a Deadly Trek to Reach the U.S. Border",
            "Julie Turkewitz", "Two crises are converging at the perilous land bridge known as the Darién Gap...")
        
        doc_2 = Document("Global Fallout From Rate Moves Won’t Stop the Fed",
            "Jeanna Smialek and Alan Rappeport", "The Federal Reserve, like many central banks...")

        docs = [doc_1, doc_2]
        db.insert_object_batch(docs)
        



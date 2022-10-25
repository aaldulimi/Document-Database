from docdb import DocDB
import dataclasses


@dataclasses.dataclass
class Document:
    title: str
    author: str
    body: str
    

if __name__ == "__main__":
    db = DocDB()
    news = db.collection("posts")

    doc_1 = Document("Global Fallout From Rate Moves Won’t Stop the Fed",
        "Jeanna Smialek and Alan Rappeport", "The Federal Reserve, like many central banks...")

    doc_2 = Document("In Record Numbers, Venezuelans Risk a Deadly Trek to Reach the U.S. Border",
        "Julie Turkewitz", "Two crises are converging at the perilous land bridge known as the Darién Gap...")

    news.insert_object(doc_1)
    news.insert_object(doc_2)


    doc_3 = {
        "title": "Another document",
        "author": "Some author with a J",
        "body": "The content of the document",
        "random": "a new field that no other document has",
        "a_number": 4
    }

    doc_id = news.insert(doc_3)
    
    print(doc_id)

   


    
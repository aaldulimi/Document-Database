from rockydb import RockyDB
import dataclasses


@dataclasses.dataclass
class Document:
    title: str
    author: str
    body: str


if __name__ == "__main__":
    db = RockyDB()
    news = db.collection("news")

    # can insert objects
    doc_1 = Document(
        "Global Fallout From Rate Moves Won’t Stop the Fed",
        "Jeanna Smialek and Alan Rappeport",
        "The Federal Reserve, like many central banks...",
    )

    doc_2 = Document(
        "In Record Numbers, Venezuelans Risk a Deadly Trek to Reach the U.S. Border",
        "Julie Turkewitz",
        "Two crises are converging at the perilous land bridge known as the Darién Gap...",
    )

    news.insert_object(doc_1)
    news.insert_object(doc_2)

    doc_3 = {
        "title": "Another document",
        "2022?": True,
        "pi": 3.14,
        "basic list": [1, 2, 3],
        "a_number": 4,
    }

    # can also insert dictionaries
    doc_id = news.insert(doc_3)

    document = news.get(doc_id)
    print(document)

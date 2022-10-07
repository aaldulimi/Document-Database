from writer import DocumentDB
from document import Document


if __name__ == "__main__":
    db = DocumentDB()

    doc_1 = Document(1, "Global Fallout From Rate Moves Won’t Stop the Fed",
        "Jeanna Smialek and Alan Rappeport", "The Federal Reserve, like many central banks...")

    doc_2 = Document(2, "In Record Numbers, Venezuelans Risk a Deadly Trek to Reach the U.S. Border",
        "Julie Turkewitz", "Two crises are converging at the perilous land bridge known as the Darién Gap...")

    db.insert(doc_1, primary_key="id")
    db.insert(doc_2, primary_key="id")

    # return document_id by searching for a specific field value 
    doc_id = db.get_id(field="author", value="Julie Turkewitz")
    print(doc_id)
from writer import DocumentDB
from document import Document



db = DocumentDB()

doc_1 = Document(1, "Global Fallout From Rate Moves Won’t Stop the Fed",
    "Jeanna Smialek and Alan Rappeport", "The Federal Reserve, like many central banks...")

doc_2 = Document(2, "In Record Numbers, Venezuelans Risk a Deadly Trek to Reach the U.S. Border",
    "Julie Turkewitz", "Two crises are converging at the perilous land bridge known as the Darién Gap...")

db.insert(doc_1, primary_key="id")
db.insert(doc_2, primary_key="id")


print(db.get("1/title"))
print(db.get("2/title"))






from database import DocumentDB
from document import Document


if __name__ == "__main__":
    db = DocumentDB("database/")

    # return all documents that match an exact value in their field 
    result = db.search(field="author", value="Julie Turkewitz")
    
    print(result)
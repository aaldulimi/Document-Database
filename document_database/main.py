from database import DocumentDB
from document import Document


if __name__ == "__main__":
    db = DocumentDB("database/")
    
    for key in db.iterate_keys():
        print(key)

    # return document by searching for a specific field value 
    result = db.search(field="author", value="Julie Turkewitz")
    print(result)
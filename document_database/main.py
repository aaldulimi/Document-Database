from database import DocumentDB
from document import Document


if __name__ == "__main__":
    db = DocumentDB("database/")

    # return all documents that match an exact value in their field 
    exact_result = db.search(field="author", value="Julie Turkewitz", type="exact")
    contains_result = db.search(field="author", value="", type="contains")
    
    print(exact_result)
    print(contains_result)
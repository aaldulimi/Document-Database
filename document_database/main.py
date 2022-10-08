from document_db import DocumentDB
from document import Document



if __name__ == "__main__":
    db = DocumentDB("database/")

    # can perform exact or contains type searches on any document field 
    exact_result = db.search(field="author", value="Julie Turkewitz", type="exact")
    contains_result = db.search(field="author", value="J", type="contains", max_count=1)

    # delete document(s) using their id
    db.delete([2])

    
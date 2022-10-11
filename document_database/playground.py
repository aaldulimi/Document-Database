from document_db import DocumentDB



if __name__ == "__main__":
    db = DocumentDB("../database/")

    # can perform exact or contains type searches on any document field 
    # exact_result = db.search(field="author", value="Julie Turkewitz", type="exact")
    # contains_result = db.search(field="author", value="J", type="contains", max_count=1)

    # delete a document using its id
    # db.delete(["1", "2", "3"])

    # get entire document using its id 
    # doc_2 = db.get_document("2")


  



    
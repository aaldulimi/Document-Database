from document_db import DocumentDB



if __name__ == "__main__":
    db = DocumentDB("../database/")

    # can perform exact or contains type searches on any document field 
    # exact_result = db.search(field="author", value="Julie Turkewitz", type="exact")
    # contains_result = db.search(field="author", value="J", type="contains", max_count=1)

    # delete a document using its id
    # db.delete("_id")

    # get entire document using its id 
    # doc_1 = db.get("7fKchz8T")

    # create an index to enable full-text search on some field(s) and then query it
    index = db.create_full_text_index(fields=["title"])
    text_search = db.text_search(index, query="Global Fallout", fields=["title"], count=2)

    
    


    

  



    
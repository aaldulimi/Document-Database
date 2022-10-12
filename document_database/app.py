from fastapi import FastAPI
from typing import Any, Dict, List, Union
from document_db import DocumentDB

app = FastAPI()


@app.get("/search/")
async def search(type: str, field: str, value: str):
    db = DocumentDB("../database")
    documents = db.search(field=field, value=value, type=type)

    return {"documents": documents}


@app.get("/document/{doc_id}")
async def get_document(doc_id):
    db = DocumentDB("../database")
    document = db.get(str(doc_id))

    return {"document": document}

@app.delete("/delete/{doc_id}")
async def delete_document(doc_id):
    db = DocumentDB("../database")
    did_delete = db.delete([doc_id])

    return {"didDelete": did_delete}



@app.post("/insert/")
async def insert_doc(document: Union[List,Dict,Any]=None):
    db = DocumentDB("../database")
    doc_id = db.insert(document)

    return {"_id": doc_id}



# TO-DO:  
# connect to db 

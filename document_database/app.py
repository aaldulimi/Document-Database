from fastapi import FastAPI
from document_db import DocumentDB

app = FastAPI()


@app.get("/search/")
async def search(type: str, field: str, value: str):
    db = DocumentDB("../database")
    results = db.search(field=field, value=value, type=type)

    return {"results": results}

# TO-DO:   
# return doc via id
# delete doc 
# insert doc
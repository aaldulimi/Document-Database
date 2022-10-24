from fastapi import FastAPI
from typing import Any, Dict, List, Union
from document_db import DocumentDB
from pydantic import BaseModel

class Settings(BaseModel):
    path: str = "../database"


app_settings = Settings()
app = FastAPI()


@app.get("/settings/info")
async def settings_info():
    return {
        "db_path": app_settings.path
    }

@app.post("/settings/update")
async def update_settings(settings: Settings):
    app_settings.path = settings.path

    return {
        "db_path": app_settings.path
    }
    

@app.get("/search/")
async def search(type: str, field: str, value: str):
    db = DocumentDB(app_settings.path)
    documents = db.search(field=field, value=value, type=type)

    return {"documents": documents}


@app.get("/document/{doc_id}")
async def get_document(doc_id):
    db = DocumentDB(app_settings.path)
    document = db.get(str(doc_id))

    return {"document": document}


@app.delete("/delete/{doc_id}")
async def delete_document(doc_id):
    db = DocumentDB(app_settings.path)
    did_delete = db.delete([doc_id])

    return {"didDelete": did_delete}


@app.post("/insert/")
async def insert_doc(document: Union[List,Dict,Any]=None):
    db = DocumentDB(app_settings.path)
    doc_id = db.insert(document)

    return {"_id": doc_id}



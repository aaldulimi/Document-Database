from fastapi import FastAPI
from typing import Any, Dict, List, Union
from rockydb.rocky import RockyDB
from pydantic import BaseModel


class Settings(BaseModel):
    db_path: str = "../database/"


app_settings = Settings()
app = FastAPI()


@app.get("/")
async def status():
    return {"status": "online"}


@app.get("/settings/info")
async def settings_info():
    return {"db_path": app_settings.db_path}


@app.post("/settings/update")
async def update_settings(settings: Settings):
    app_settings.db_path = settings.db_path

    return {"db_path": app_settings.db_path}


@app.get("/{collection_name}/search/")
async def search(collection_name, type: str, field: str, value: str):
    collection = RockyDB(app_settings.db_path).collection(collection_name)
    documents = collection.search(field=field, value=value, type=type)

    return {"documents": documents}


@app.get("/{collection_name}/document/{doc_id}")
async def get_document(collection_name: str, doc_id):
    collection = RockyDB(app_settings.db_path).collection(collection_name)
    document = collection.get(str(doc_id))

    return {"document": document}


@app.delete("/{collection_name}/delete/{doc_id}")
async def delete_document(collection_name: str, doc_id):
    collection = RockyDB(app_settings.db_path).collection(collection_name)
    did_delete = collection.delete([doc_id])

    return {"didDelete": did_delete}


@app.post("/{collection_name}/insert/")
async def insert_doc(collection_name: str, document: Union[List, Dict, Any] = None):
    collection = RockyDB(app_settings.db_path).collection(collection_name)
    doc_id = collection.insert(document)

    return {"_id": doc_id}

from typing import Optional
import tantivy
import json
from pathlib import Path
from rocksdict import Rdict

class Index():
    def __init__(self, db_path, collection, name: str, fields : Optional[list] = None):
        self.name = name 
        self.fields = fields 
        self.db_path = db_path
        self.collection = collection
    

    def _get(self, key: str):
        return self.collection[key]
    

    def _create_dir(self, dir_path, with_meta: bool = False):
        if Path(dir_path).is_dir():
            return False

        # make directory 
        db_path = Path(dir_path)
        db_path.mkdir(parents=True, exist_ok=True)

        # make meta file 
        if with_meta:
            with open(dir_path + "/meta.json", "w") as f:
                json.dump([], f, indent=4)
        
        return True

    def _delete_old_logs(self):
        database_path = Path(self.db_path)    
        database_files = list(database_path.iterdir())
        
        for filename in database_files:
            if filename.name[:7] == "LOG.old":
                filename.unlink()


    def _iterate_keys(self):
        for key in self.collection.keys():
            yield key
        
        self._delete_old_logs()


    def _add_index(self, index_specs):
        meta_file = self.db_path + "/full_text/meta.json"

        with open(meta_file) as f:
            index_data = json.load(f)

        index_data.append(index_specs)

        with open(meta_file, "w") as f:
            json.dump(index_data, f, indent=4)
        

    def _check_index_exists(self, index_name):
        self._create_dir(self.db_path + "/full_text", with_meta=True)

        if Path(self.db_path + "/full_text/" + index_name).is_dir():
            return True

        return False


    def get_index(self, index_name):
        schema_builder = tantivy.SchemaBuilder()
        schema_builder.add_text_field("_id", stored=True)

        with open(self.db_path + "/full_text/meta.json") as f:
            index_data = json.load(f)

        for index in index_data:
            if index["name"] == index_name:
                for field in index["schema"]:
                    if field != "_id": schema_builder.add_text_field(field, stored=False)
                    
                index_path = index["path"]

        schema = schema_builder.build()
        index = tantivy.Index(schema, path=index_path)
        
        return index

    def create(self):
        if self._check_index_exists(self.name):
            print(f"Index: {self.name} already exists.")
            return self.get_index(self.name)
        
        if not self.fields:
            print("Specify fields to index using the fields parameter i.e. create(name, fields=[])")
            return None 

        index_path = self.db_path + "/full_text/" + self.name

        index_specs = {
            "name": self.name,
            "schema": ["_id"],
            "path": index_path
        }

        schema_builder = tantivy.SchemaBuilder()
        schema_builder.add_text_field("_id", stored=True)

        for field in self.fields:
            schema_builder.add_text_field(field, stored=False)
            index_specs["schema"].append(field)
            
        schema = schema_builder.build()

        self._create_dir(index_path)
        self._add_index(index_specs)

        index = tantivy.Index(schema, path=index_path)
        writer = index.writer()

        current_doc_id = ""
        current_doc = {}

        for key in self._iterate_keys():
            seperated_key = key.split("/")
            doc_id = seperated_key[0]
            key_column = seperated_key[1]

            if doc_id != current_doc_id:
                if current_doc:
                    # append doc to index
                    current_doc["_id"] = [current_doc_id]

                    writer.add_document(tantivy.Document(**current_doc))
                    writer.commit()
                    
                current_doc = {}
                current_doc_id = doc_id

            if key_column in self.fields:
                key_value = self._get(key)
                
                if key_value:
                    current_doc[key_column] = key_value
        
       
        return index

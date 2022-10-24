from pathlib import Path
import tantivy
import json
import string
from rocksdict import Rdict
import random

class Collection():
    def __init__(self, db_path: str, name: str):
        self.db_path = db_path
        self.name = name
        self.path = self.db_path + name

        print(self.path)

        self._create_dir(self.path, with_meta=False)
        self.collection = Rdict(self.path)
        

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
    
    def _add_index(self, index_specs):
        meta_file = self.path + "/full_text/meta.json"

        with open(meta_file) as f:
            index_data = json.load(f)

        index_data.append(index_specs)

        with open(meta_file, "w") as f:
            json.dump(index_data, f, indent=4)
        

    def _check_index_exists(self, index_name):
        self._create_dir(self.path + "/full_text", with_meta=True)

        if Path(self.path + "/full_text/" + index_name).is_dir():
            return True

        return False


    def get_index(self, index_name):
        schema_builder = tantivy.SchemaBuilder()
        schema_builder.add_text_field("_id", stored=True)

        with open(self.path + "/full_text/meta.json") as f:
            index_data = json.load(f)

        for index in index_data:
            if index["name"] == index_name:
                for field in index["schema"]:
                    if field != "_id": schema_builder.add_text_field(field, stored=False)
                    
                index_path = index["path"]

        schema = schema_builder.build()
        index = tantivy.Index(schema, path=index_path)
        
        return index
    


    def create_full_text_index(self, index_name, fields):
        if self._check_index_exists(index_name):
            return self.get_index(index_name)
             

        index_specs = {
            "name": index_name,
            "schema": ["_id"],
            "path": ""
        }

        schema_builder = tantivy.SchemaBuilder()
        schema_builder.add_text_field("_id", stored=True)

        for field in fields:
            schema_builder.add_text_field(field, stored=False)
            index_specs["schema"].append(field)
            
        schema = schema_builder.build()

        index_path = self.path + "/full_text/" + index_name
        index_specs["path"] = index_path

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

            if key_column in fields:
                key_value = self._get(key)
                
                if key_value:
                    current_doc[key_column] = key_value
        
       
        return index
    

    
    def _delete_old_logs(self):
        database_path = Path(self.path)    
        database_files = list(database_path.iterdir())
        
        for filename in database_files:
            if filename.name[:7] == "LOG.old":
                filename.unlink()
             

    def _generate_id(self):
        characters = string.ascii_letters + string.digits 
        doc_id = ''.join(random.choice(characters) for i in range(8))

        return doc_id


    def insert_object(self, document):
        document_dict = document.__dict__.copy()
        doc_id = self.insert(document_dict)

        return doc_id


    def insert(self, document):
        # encoding: 
        # doc_id/column_name -> value 

        if "_id" not in document:
            document["_id"] = self._generate_id()
        
        doc_id = document["_id"]

        for key, value in document.items():
            if key != "_id":
                key_string = f"{doc_id}/{key}"
                self.collection[key_string] = value

        # self._delete_old_logs()
        return doc_id


    def insert_batch(self, document_list):
        for document in document_list:
            self.insert(document)


    def insert_object_batch(self, object_list):
        for object in object_list:
            self.insert_object(object)


    def _get(self, key):
        return self.collection[key]

    
    def _iterate_keys(self):
        for key in self.collection.keys():
            yield key
        
        self._delete_old_logs()

    def get_id_exact(self, field, value, max_count: int = None):
        all_ids = []

        for key in self._iterate_keys():
            
            key_column = key.split("/")[1]
            
            if field == key_column:
                if value == self._get(key):
                    row_id = key.split("/")[0]
                    all_ids.append(row_id)
        
            if max_count:
                if len(all_ids) == max_count:
                    return all_ids
        
        return all_ids
                    

    def get_id_contains(self, field, value, max_count: int = None):
        all_ids = []

        for key in self._iterate_keys():
            
            key_column = key.split("/")[1]
            key_value = self._get(key)

            if (field == key_column) and key_value:
                if value in self._get(key):
                    row_id = key.split("/")[0]
                    all_ids.append(row_id)
        
            if max_count:
                if len(all_ids) == max_count:
                    return all_ids
        
        return all_ids

    def _contains(self, field, value, max_count: int = None):
        results = []
        doc_ids = self.get_id_contains(field, value, max_count)

        if doc_ids:
            for doc_id in doc_ids:
                doc_dict = {}
                doc_dict["_id"] = doc_id
                
                for key in self._iterate_keys():
                    search_doc_id = key.split("/")[0]

                    if (search_doc_id == doc_id):

                        column_name = key.split("/")[1]
                        doc_dict[column_name] = self._get(key)

                results.append(doc_dict)

        return results

    
    def _exact(self, field, value, max_count: int = None):
        results = []
        doc_ids = self.get_id_exact(field, value, max_count)

        if doc_ids:
            for doc_id in doc_ids:
                doc_dict = {}
                doc_dict["_id"] = doc_id
                
                for key in self._iterate_keys():
                    search_doc_id =  key.split("/")[0]

                    if (search_doc_id == doc_id):
                        column_name = key.split("/")[1]
                        doc_dict[column_name] = self._get(key)

                results.append(doc_dict)

        return results


    def search(self, field, value, type: str = "exact", max_count: int = None):
        if type == "exact":
            results = self._exact(field, value, max_count)
        
        elif type == "contains":
            results = self._contains(field, value, max_count)
        
        else:
            print(f"Wrong search type specified. Must specifiy 'exact' or 'contains' not {type}\n")
            return None

        self._delete_old_logs()
        return results

    
    def text_search(self, index, query: str, fields, count: int = 2):
        results = []

        searcher = index.searcher()
        parsed_query = index.parse_query(query, fields)

        text_results = searcher.search(parsed_query, count).hits

        for result in text_results:
            score, address = result
            document_id = searcher.doc(address)["_id"][0]

            results.append(self.get(document_id))

        return results

    

    def delete(self, id):
        did_delete = False

        for key in self._iterate_keys():
            doc_id = key.split("/")[0]

            if id == doc_id:
                self.collection[key] = None
                did_delete = True

        self._delete_old_logs()
        return did_delete


    def delete_batch(self, id_list):
        for id in id_list:
            self.delete(id)
        
    
    def get(self, id):
        document = {}

        for key in self._iterate_keys():
            search_doc_id = key.split("/")[0]

            if (search_doc_id == id):
                column_name = key.split("/")[1]
                document[column_name] = self._get(key)

        if document:
            document["_id"] = id

        return document
    

    def get_batch(self, id_list):
        results = []

        for id in id_list:
            document = self.get(id)
            results.append(document)

        return results

    
    







            
from pathlib import Path
import tantivy
import json
import string
from rocksdict import Rdict, Options
import random
from index import Index
from typing import Optional
import encoding 

class Collection():
    def __init__(self, db_path: str, name: str):
        self.db_path = db_path
        self.name = name
        self.path = self.db_path + name

        self._create_dir(self.path, with_meta=False)
        self.collection = Rdict(path=self.path, options=Options(raw_mode=True))

        self.encoding_types = {
            str: 0,
            int: 1,
            float: 2,
            bool: 3,
            list: 4,
            "0": str,
            "1": int,
            "2": float,
            "3": bool,
            "4": list,
        }

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
        # current encoding: 
        # doc_id/column_name -> value 

        # new encoding (not yet implemented)
        # collection_id/doc_id/col_id -> datatype_id/value 

        if "_id" not in document:
            document["_id"] = self._generate_id()
        
        doc_id = document["_id"]

        for key, value in document.items():
            if key != "_id":
                key_string = f"{self.name}/{doc_id}/{key}"
                value_string = f'{self.encoding_types[type(value)]}/{value}'

                encoded_key = encoding.encode_str(key_string)
                encoded_value = encoding.encode_str(value_string)

                self.collection[encoded_key] = encoded_value

        # self._delete_old_logs()
        return doc_id


    def insert_batch(self, document_list):
        for document in document_list:
            self.insert(document)


    def insert_object_batch(self, object_list):
        for object in object_list:
            self.insert_object(object)


    def _get(self, key):
        decoded_value = encoding.decode_str(self.collection[key]).split("/")
        decoded_type = decoded_value[0]
        decoded_value = decoded_value[1]

        return self.encoding_types[decoded_type](decoded_value)

    
    def _iterate_keys(self):
        for key in self.collection.keys():
            yield key
        
        self._delete_old_logs()

    
    def index(self, name: str, fields: Optional[list] = None):
        index = Index(self.path, self.collection, name, fields).create()

        return index


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

    
    def text_search(self, index: tantivy.Index, query: str, fields: list, count: int = 2):
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
            decoded_key = encoding.decode_str(key).split("/")
            search_doc_id = decoded_key[1]

            if (search_doc_id == id):
                column_name = decoded_key[2]
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


    def destroy(self):
        Rdict.destroy(self.path)


    
    







            
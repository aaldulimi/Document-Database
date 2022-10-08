from rocksdict import Rdict 
import re


class DocumentDB():
    counter = 0

    def __init__(self, path: str = "database/"):
        self.db = Rdict(path)
        
    def insert(self, document):
        # encoding: primary_key/column_name -> value 
        DocumentDB.counter += 1
        document_dict = document.__dict__

        if "id" not in document_dict:
            document["id"] = DocumentDB.counter
        
        doc_id = document_dict["id"]

        for key, value in document_dict.items():
            if key != "id":
                key_string = f"{doc_id}/{key}"
                self.db[key_string] = value

    
    def get(self, key):
        return self.db[key]

    
    def iterate_keys(self):
        for key in self.db.keys():
            yield key

    def get_id(self, field, value):
        for key in self.iterate_keys():
            key_column = re.findall("[^/]*", key)[2]

            if field == key_column:
                if value == self.get(key):
                    return re.findall("[^/]*", key)[0]


    def search(self, field, value):
        doc_dict = {}
        doc_id = self.get_id(field, value)

        if doc_id:
            doc_dict["id"] = doc_id
            
            for key in self.iterate_keys():
                search_doc_id = re.findall("[^/]*", key)[0]

                if search_doc_id == doc_id:
                    column_name = re.findall("[^/]*", key)[2]
                    doc_dict[column_name] = self.get(key)

    
        return doc_dict

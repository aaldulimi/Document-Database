from rocksdict import Rdict 
import re


class DocumentDB():
    counter = 0

    def __init__(self, path: str = "database/"):
        self.db = Rdict(path)
        
    def insert(self, document):
        # encoding: primary_key/column_name -> value 
        DocumentDB.counter += 1
        document_dict = document.__dict__.copy()

        if "id" not in document_dict:
            document_dict["id"] = DocumentDB.counter
        
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

    def get_id_exact(self, field, value, max_count: int = None):
        all_ids = []

        for key in self.iterate_keys():
            key_column = re.findall("[^/]*", key)[2]

            if field == key_column:
                if value == self.get(key):
                    row_id = re.findall("[^/]*", key)[0]
                    all_ids.append(row_id)
        
            if max_count:
                if len(all_ids) == max_count:
                    return all_ids
        
        return all_ids
                    

    def get_id_contains(self, field, value, max_count: int = None):
        all_ids = []

        for key in self.iterate_keys():
            key_column = re.findall("[^/]*", key)[2]

            if field == key_column:
                if value in self.get(key):
                    row_id = re.findall("[^/]*", key)[0]
                    all_ids.append(row_id)
        
            if max_count:
                if len(all_ids) == max_count:
                    return all_ids
        


    def _contains(self, field, value):
        pass
    
    def _exact(self, field, value):
        results = []
        doc_ids = self.get_id_exact(field, value)

        if doc_ids:
            for doc_id in doc_ids:
                doc_dict = {}
                doc_dict["id"] = doc_id
                
                for key in self.iterate_keys():
                    search_doc_id = re.findall("[^/]*", key)[0]

                    if search_doc_id == doc_id:
                        column_name = re.findall("[^/]*", key)[2]
                        doc_dict[column_name] = self.get(key)

                results.append(doc_dict)

        return results


    def search(self, field, value):
        results = self._exact(field, value)

        return results
    
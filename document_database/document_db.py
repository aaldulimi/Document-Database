from rocksdict import Rdict 
import re


class DocumentDB():
    counter = 0

    def __init__(self, path: str = "database/"):
        self.db = Rdict(path)
        
    def insert_object(self, document):
        document_dict = document.__dict__.copy()
        self.insert(document_dict)


    def insert(self, document):
        # encoding: primary_key/column_name -> value 
        DocumentDB.counter += 1

        if "id" not in document:
            document["id"] = DocumentDB.counter
        
        doc_id = document["id"]

        for key, value in document.items():
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
            key_value = self.get(key)

            if (field == key_column) and key_value:
                if value in self.get(key):
                    row_id = re.findall("[^/]*", key)[0]
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
                doc_dict["id"] = doc_id
                
                for key in self.iterate_keys():
                    search_doc_id = re.findall("[^/]*", key)[0]

                    if search_doc_id == doc_id:
                        column_name = re.findall("[^/]*", key)[2]
                        doc_dict[column_name] = self.get(key)

                results.append(doc_dict)

        return results

    
    def _exact(self, field, value, max_count: int = None):
        results = []
        doc_ids = self.get_id_exact(field, value, max_count)

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


    def search(self, field, value, type: str = "exact", max_count: int = None):
        if type == "exact":
            results = self._exact(field, value, max_count)
        
        elif type == "contains":
            results = self._contains(field, value, max_count)
        
        else:
            print(f"Wrong search type specified. Must specifiy 'exact' or 'contains' not {type}\n")
            return None

        return results
    
    def _delete(self, id):
        for key in self.iterate_keys():
            doc_id = re.findall("[^/]*", key)[0]

            if str(id) == doc_id:
                self.db[key] = None


    def delete(self, id_list):
        for id in id_list:
            self._delete(id)

            
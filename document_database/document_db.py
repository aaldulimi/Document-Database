from rocksdict import Rdict 
import random
import string 
from pathlib import Path
import tantivy
import json


class DocumentDB():
    def __init__(self, path: str = "../database/"):
        self.path = path

        self._create_dir(self.path)
        self.db = Rdict(path)


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

    
    def _delete_db_files(self, delete_index: bool = False):
        database_path = Path(self.path)    
        database_files = list(database_path.iterdir())
        
        for filename in database_files:
            filename.unlink()
        
        if delete_index: self._delete_tantivy_files()
    

    def _delete_tantivy_files(self):
        tantivy_path = Path(self.path + "/full_text/")    
        tantivy_files = list(tantivy_path.iterdir())
        
        for filename in tantivy_files:
            filename.unlink()

    
    def delete_all(self):
        self._delete_db_files(True)







            
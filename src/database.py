from pathlib import Path
from collection import Collection


class DocDB():
    def __init__(self, path: str = "database/"):
        self.path = path
        self._create_dir(self.path)
        

    def _create_dir(self, dir_path: str, with_meta: bool = False) ->  bool:
        if Path(dir_path).is_dir():
            return False

        # make directory 
        db_path = Path(dir_path)
        db_path.mkdir(parents=True, exist_ok=True)

        return True


    def collection(self, name: str):
        return Collection(self.path, name)


    def delete_database(self):
        database_path = Path(self.path)    
        database_files = list(database_path.iterdir())
        
        for filename in database_files:
            filename.unlink()
        
    






            
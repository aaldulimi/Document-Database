from pathlib import Path
from src.collection import Collection


class RockyDB:
    def __init__(self, path: str = "database/"):
        self.path = path
        self._create_dir(self.path)

    def _create_dir(self, dir_path: str, with_meta: bool = False) -> bool:
        if Path(dir_path).is_dir():
            return False

        # make directory
        db_path = Path(dir_path)
        db_path.mkdir(parents=True, exist_ok=True)

        return True

    def collection(self, name: str):
        # add to meta.json file that belongs to db (outside of all collections)
        return Collection(self.path, name)

    def destroy(self):
        database_path = Path(self.path)
        database_files = list(database_path.iterdir())

        for filename in database_files:
            filename.unlink()
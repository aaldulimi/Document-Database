from rocksdict import Rdict 



class DocumentDB():
    def __init__(self, path: str = "database/"):
        self.db = Rdict(path)


    def insert(self, document):
        for key, value in document.__dict__.items():
            self.db[key] = value

    
    def get(self, key):
        return self.db[key]

import rockydb.encoding as encoding
from rocksdict import ReadOptions

class Index():
    def __init__(self, collection, name: str, collection_name: str, index_id: int, field: str):
        self.collection = collection
        self.name = name
        self.field = field
        self.id = index_id
        self.collection_name = collection_name

    def _iter_default_db(self):
        key = encoding.encode_str(self.collection_name + "/0/0/")
        iter = self.collection.iter(ReadOptions(raw_mode=True))
        iter.seek(key)

        if not iter.key():
            return 

        while iter.valid():
            encoded_key = iter.key()
            encoded_value = iter.value()
            # decoded_key = encoding.decode_str(encoded_key).split("/")
    
            yield (encoded_key, encoded_value)
            iter.next()

    def create(self):
        # implement some sort algo that doesn't require all the data to be in memory
        # for now, brute force it; read 100 rows, insert in dict and sort, insert into dummy db
        i = 0
        block_id = 1
        
        block = {}
        for k, v in self._iter_default_db():
            block[k] = v
            i += 1

            if i == 100:
                block_sorted = dict(sorted(block.items(), key=lambda item: item[1]))
                self._insert_tmp_kv(block_id, block_sorted)
                block_id += 1
                i = 0
                block = {}

        # add remaining kv
        if block:
            block_sorted = dict(sorted(block.items(), key=lambda item: item[1]))
            self._insert_tmp_kv(block_id, block_sorted)


        # now merge sort all the blocks together
        self._merge_block(block_id)


        index_specs = {"name": self.name, "field": self.field}
        return index_specs
    

    def _insert_tmp_kv(self, id, kv_pairs):
        i = 0

        for k, v in kv_pairs.items():
            pre_key = encoding.encode_str(f"tmp/{id}/")
            key = pre_key + k

            self.collection[key] = v
            i += 1
        
        return

    def _merge_block(self, block_count: int):
        for i in range(1, block_count):
            pass
            
       

    def binary_search(self, value):
        pass


    
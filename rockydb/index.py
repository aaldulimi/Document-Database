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
            decoded_key = encoding.decode_str(encoded_key).split("/")

            if decoded_key[4] == self.field:
                yield (decoded_key[3], encoded_value)

            iter.next()

    def create(self):
        # implement some sort algo that doesn't require all the data to be in memory
        # for now, brute force it; read 100 rows, insert in dict and sort, insert into dummy db
        i = 0
        block_id = 0
        
        # tmp/block_id/order_no/doc_id -> datatype_id/value
        block = {}
        for k, v in self._iter_default_db():
            tmp_key = encoding.encode_str(f"tmp/{block_id}/{i}/{k}")
            block[tmp_key] = v
            i += 1

            if i == 100:
                block_sorted = dict(sorted(block.items(), key=lambda item: item[1]))
                self._insert_tmp_kv(block_sorted)
                block_id += 1
                i = 0
                block = {}

        # add remaining kv
        if block:
            block_sorted = dict(sorted(block.items(), key=lambda item: item[1]))
            self._insert_tmp_kv(block_id, block_sorted)


        # now merge sort all the blocks together
        self._merge_blocks(block_id)


        index_specs = {"name": self.name, "field": self.field}
        return index_specs
    

    def _insert_tmp_kv(self, kv_pairs: dict):
        # insert all blocks of sorted kv pairs back into db
        for k, v in kv_pairs.items():
            self.collection[k] = v
        

    def _merge_blocks(self, block_count: int):
        # merge all blocks together, have pointers to start of blocks
        # take first key from each block, compare, insert smallest into new db
        iter = self.collection.iter(ReadOptions(raw_mode=True))


        first_key = encoding.encode_str(f"tmp/0/0/")
        iter.seek(key)

        
        for i in range(block_count + 1):
            key = encoding.encode_str(f"tmp/{i}/0/")
            
       

    def binary_search(self, value):
        pass


    
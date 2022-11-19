import rockydb.encoding as encoding
from rocksdict import ReadOptions


class Index:
    def __init__(
        self, collection, collection_name: str, name: str, index_id: int, field: str
    ):
        self.collection = collection
        self.name = name
        self.field = field
        self.id = index_id
        self.collection_name = collection_name
        self.key_count = 0

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

            if decoded_key[0] != self.collection_name:
                break

            if decoded_key[4] == self.field:
                # returns (doc_id, bytes)
                yield (decoded_key[3], encoded_value)

            iter.next()

    def _iter_index_db(self, start: int = 0, limit: int = None):
        # returns doc_id
        if limit is None:
            limit = self.key_count - 1

        while 1:
            encoded_key = encoding.encode_str(f"{self.id}/{start}")
            decoded_key = encoding.decode_str(encoded_key).split("/")

            # make sure its not over the limit, to prevent key not found errors
            if int(decoded_key[1]) > limit:
                break

            encoded_value = self.collection[encoded_key]
            if not encoded_value:
                return

            doc_id = encoding.decode_str(encoded_value[1:])
            yield doc_id

            start += 1

    def create(self):
        # implement some sort algo that doesn't require all the data to be in memory
        # for now, brute force it; read 100 rows, insert in dict and sort, insert into dummy db
        i = 0
        block_id = 0

        # tmp/block_id/order_no/doc_id -> datatype_id/value
        block = {}
        for k, v in self._iter_default_db():
            tmp_key = f"{block_id}/{k}"
            block[tmp_key] = v
            i += 1

            if i == 100:
                block_sorted = dict(sorted(block.items(), key=lambda item: item[1]))
                block_rename = self._rename_block_keys(block_sorted)
                self._insert_tmp_kv(block_rename)
                block_id += 1
                i = 0
                block = {}

        # add remaining kv
        if block:
            block_sorted = dict(sorted(block.items(), key=lambda item: item[1]))
            block_renamed = self._rename_block_keys(block_sorted)
            self._insert_tmp_kv(block_renamed)
            block_id += 1

        # now merge sort all the blocks together
        self._merge_blocks(block_id)

        index_specs = {"name": self.name, "field": self.field, "id": self.id}
        return index_specs

    def _rename_block_keys(self, block: dict):
        result = {}
        i = 0

        for key, value in block.items():
            # current key: str block_id/doc_id, need to be tmp/block_id/order_no/doc_id
            split_key = key.split("/")
            new_key = f"tmp/{split_key[0]}/{i}/{split_key[1]}"

            result[new_key] = value
            i += 1

        return result

    def _insert_tmp_kv(self, kv_pairs: dict):
        # insert all blocks of sorted kv pairs back into db
        for k, v in kv_pairs.items():
            k = encoding.encode_str(k)
            self.collection[k] = v

    def _merge_blocks(self, block_count: int):
        # merge all blocks together, have pointers to start of blocks
        # take first key from each block, compare, insert smallest into new db
        iter = self.collection.iter(ReadOptions(raw_mode=True))

        base_block = 0

        # keep track of all pointer positions
        block_i_count = [0 for _ in range(block_count)]
        block_id_increment = 0

        while 1:
            # make sure base block is not complete
            if block_i_count[base_block] <= -1:
                for block_id in range(block_count):
                    if block_i_count[block_id] != -1:
                        base_block = block_id
                        block_id_increment = base_block
                        break

                if block_i_count[base_block] <= -1:
                    break

            base_key = encoding.encode_str(
                f"tmp/{base_block}/{block_i_count[base_block]}/"
            )
            iter.seek(base_key)
            k = iter.key()
            k_value = iter.value()

            for block_id in range(block_count):
                # for each block, start at first key and iterate through all other 99 keys
                # check if block is complete, if so, skip it
                if block_i_count[block_id] <= -1:
                    continue

                block_key = encoding.encode_str(
                    f"tmp/{block_id}/{block_i_count[block_id]}/"
                )
                iter.seek(block_key)
                block_k_value = iter.value()
                block_key = iter.key()

                # iter.seek() will go to the next key if the key doesn't exist, however we want to skip the block if the key doesn't exist
                should_be_key = f"tmp/{block_id}/{block_i_count[block_id]}"
                if (
                    encoding.decode_str(block_key)[: len(should_be_key)]
                    != should_be_key
                ):
                    block_i_count[block_id] = -2
                    continue

                # this should be fixed in earlier stages, set None to 0
                if block_k_value is None:
                    continue

                # if block value is shorter than the base value, then insert that instead
                if block_k_value < k_value:
                    k = block_key
                    k_value = block_k_value
                    block_id_increment = block_id

            # increment pointer for the block we just go the value from
            block_i_count[block_id_increment] += 1

            if block_i_count[block_id_increment] != -1:
                # found the smallest key between all pointers, insert into new db,
                # index_id/order_no -> str/doc_id
                new_key = encoding.encode_str(f"{self.id}/{self.key_count}")
                decoded_doc_id = encoding.decode_str(k).split("/")[3]
                encoded_doc_id = encoding.encode_str(decoded_doc_id)
                encoded_data_type = encoded_data_type = encoding.encode_int(
                    1
                )  # encode id for str is 1

                self.collection[new_key] = encoded_data_type + encoded_doc_id
                self.key_count += 1

            # if block is complete, set to -1
            if block_i_count[block_id_increment] == 100:
                block_i_count[block_id_increment] = -1

                # if block is complete, use another block as the new base key
                found_new_block = 0
                for i in range(block_count):
                    if block_i_count[i] != -1:
                        base_block = block_id_increment
                        found_new_block = 1
                        break

                if not found_new_block:
                    # we have iterated through all blocks, no new blocks have been found all keys have been inserted in order
                    break

            else:
                # otherwise, set the new base key to be from the block that we inserted from
                base_block = block_id_increment

    def _parse_query(self, query: dict):
        lt = 0
        lte = 0
        gt = 0
        gte = 0
        eq = 0
        # need to iterate over keys and values once only
        for spec, v in query.items():
            q_loc = spec.find("?")

            if q_loc != -1:
                query_type = spec[q_loc + 1 :]

                # can only be of one type below
                if query_type == "lte":
                    lte = encoding.encode_int(v)
                    continue

                if query_type == "gte":
                    gte = encoding.encode_int(v)
                    continue

                if query_type == "lt":
                    lt = encoding.encode_int(v)
                    continue

                if query_type == "gt":
                    gt = encoding.encode_int(v)
                    continue

            else:
                # add to equals dict
                eq[spec] = v

        return (lt, lte, gt, gte, eq)

    def find(self, query: dict, limit: int = 1):
        results = []
        if not query or not limit:
            return results

        lt, lte, gt, gte, eq = self._parse_query(query)

        # if query is less than, e.g. { "age?lte":  30 }
        if lte:
            index_id = self.less_than_equals(lte)
            for doc_id in self._iter_index_db(start=0, limit=index_id):
                results.append(doc_id)

            return results

        if gte:
            index_id = self.greater_than_equals(gte)
            for doc_id in self._iter_index_db(start=index_id, limit=None):
                results.append(doc_id)

            return results

        if lt:
            index_id = self.less_than(lt)
            for doc_id in self._iter_index_db(start=0, limit=index_id):
                results.append(doc_id)

            return results

        if gt:
            index_id = self.greater_than(gt)
            for doc_id in self._iter_index_db(start=index_id, limit=None):
                results.append(doc_id)

            return results

        return results

    def _get_value_from_index_key(self, key: str) -> bytes:
        index_key = encoding.encode_str(key)
        index_value = self.collection[index_key]
        doc_id = encoding.decode_str(index_value[1:])

        db_key = encoding.encode_str(
            f"{self.collection_name}/0/0/{doc_id}/{self.field}"
        )
        db_value = self.collection[db_key]

        return db_value

    def less_than_equals(self, target: bytes) -> int:
        # for lte type search, also know as last occurance
        min = 0
        max = self.key_count

        while min <= max:
            mid = (min + max) // 2
            mid_value = self._get_value_from_index_key(f"{self.id}/{mid}")[
                1:
            ]  # bytes of value
            mid_value_plus_one = self._get_value_from_index_key(f"{self.id}/{mid + 1}")[
                1:
            ]  # bytes of value

            if ((mid == self.key_count) or (mid_value_plus_one > target)) and (
                mid_value == target
            ):
                return mid

            elif target < mid_value:
                max = mid - 1

            else:
                min = mid + 1

        if min < max:
            return min
        return max

    def greater_than_equals(self, target: bytes) -> int:
        # for gte type search, also known as first occurance
        min = 0
        max = self.key_count

        while min < max:
            mid = (min + max) // 2
            mid_value = self._get_value_from_index_key(f"{self.id}/{mid}")[1:]
            mid_value_minus_one = self._get_value_from_index_key(
                f"{self.id}/{mid - 1}"
            )[1:]

            if ((mid == self.key_count) or (mid_value_minus_one < target)) and (
                mid_value == target
            ):
                return mid

            elif target > mid_value:
                min = mid + 1

            else:
                max = mid

        return min

    def less_than(self, target: bytes) -> int:
        # for lt type search
        min = 0
        max = self.key_count

        while min < max:
            mid = (min + max) // 2
            mid_value = self._get_value_from_index_key(f"{self.id}/{mid}")[1:]
            mid_value_plus_one = self._get_value_from_index_key(f"{self.id}/{mid + 1}")[
                1:
            ]

            if ((mid == self.key_count) or (mid_value_plus_one >= target)) and (
                mid_value < target
            ):
                return mid

            elif mid_value >= target:
                max = mid - 1

            else:
                min = mid + 1

        return min

    def greater_than(self, target: bytes) -> int:
        # for gt type search
        min = 0
        max = self.key_count

        while min < max:
            mid = (min + max) // 2
            mid_value = self._get_value_from_index_key(f"{self.id}/{mid}")[1:]
            mid_value_minus_one = self._get_value_from_index_key(
                f"{self.id}/{mid - 1}"
            )[1:]

            if (mid_value_minus_one <= target) and (mid_value > target):
                return mid

            elif mid_value <= target:
                min = mid + 1

            else:
                max = mid

        return min

    def get(self, id: str) -> dict:
        document = {}

        for encoded_key in self._id_rows(id):
            decoded_key = encoding.decode_str(encoded_key).split("/")

            column = decoded_key[4]
            document[column] = self._get(encoded_key)

        if not document:
            return None

        document["_id"] = id
        return document

    def _id_rows(self, id: str):
        key = encoding.encode_str(self.collection_name + "/0/0/" + id)
        iter = self.collection.iter(ReadOptions(raw_mode=True))
        iter.seek(key)

        if not iter.key():
            return {}

        while iter.valid():
            encoded_key = iter.key()
            decoded_key = encoding.decode_str(encoded_key).split("/")
            if decoded_key[3] != id:
                break

            yield encoded_key
            iter.next()

    def _decode_value(self, value: bytes):
        if not value:
            return None

        decoded_value = encoding.decode_this(str, value[1:])
        return decoded_value

    def _get(self, key: bytes):
        value = self.collection[key]
        return self._decode_value(value)

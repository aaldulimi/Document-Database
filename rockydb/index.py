# from typing import Optional
# import tantivy
# import json
# from pathlib import Path
# import rockydb.encoding as encoding
# from rocksdict import ReadOptions, Rdict


# class Index:
#     def __init__(
#         self,
#         db_path: str,
#         collection: Rdict,
#         collection_name: str,
#         name: str,
#         fields: Optional[list] = None,
#         encoding_types: dict = None,
#     ):

#         self.name = name
#         self.fields = fields
#         self.db_path = db_path
#         self.collection = collection
#         self.collection_name = collection_name
#         self.encoding_types = encoding_types

#     def _decode_value(self, value: bytes):
#         if not value:
#             return None

#         decoded_data_type = self.encoding_types[value[0]]
#         decoded_value = encoding.decode_this(decoded_data_type, value[1:])

#         return decoded_value

#     def _get(self, key: bytes):
#         value = self.collection[key]
#         return self._decode_value(value)

#     def get(self, id: str):
#         document = {}

#         key = encoding.encode_str(self.collection_name + "/" + id)
#         iter = self.collection.iter(ReadOptions(raw_mode=True))
#         iter.seek(key)

#         if not iter.key():
#             return {}

#         while iter.valid():
#             encoded_key = iter.key()
#             encoded_value = iter.value()

#             decoded_key = encoding.decode_str(encoded_key).split("/")
#             column = decoded_key[2]
#             document[column] = self._decode_value(encoded_value)

#             iter.next()

#         if not document:
#             return None

#         document["_id"] = id
#         return document

#     def _create_dir(self, dir_path: str, with_meta: bool = False):
#         if Path(dir_path).is_dir():
#             return False

#         # make directory
#         db_path = Path(dir_path)
#         db_path.mkdir(parents=True, exist_ok=True)

#         # make meta file
#         if with_meta:
#             with open(dir_path + "/meta.json", "w") as f:
#                 json.dump([], f, indent=4)

#         return True

#     def _delete_old_logs(self):
#         database_path = Path(self.db_path)
#         database_files = list(database_path.iterdir())

#         for filename in database_files:
#             if filename.name[:7] == "LOG.old":
#                 filename.unlink()

#     def _iterate_keys(self):
#         for key in self.collection.keys():
#             yield key

#         self._delete_old_logs()

#     def _add_index(self, index_specs: dict):
#         meta_file = self.db_path + "/full_text/meta.json"

#         with open(meta_file) as f:
#             index_data = json.load(f)

#         index_data.append(index_specs)

#         with open(meta_file, "w") as f:
#             json.dump(index_data, f, indent=4)

#     def _check_index_exists(self, index_name: str):
#         self._create_dir(self.db_path + "/full_text", with_meta=True)

#         if Path(self.db_path + "/full_text/" + index_name).is_dir():
#             return True

#         return False

#     def get_index(self, index_name: str, with_schema: bool = True):
#         fetched_schema = []
#         schema_builder = tantivy.SchemaBuilder()
#         schema_builder.add_text_field("_id", stored=True)

#         with open(self.db_path + "/full_text/meta.json") as f:
#             index_data = json.load(f)

#         for index in index_data:
#             if index["name"] == index_name:
#                 for field in index["schema"]:
#                     if field != "_id":
#                         schema_builder.add_text_field(field, stored=False)

#                 if with_schema:
#                     fetched_schema = index["schema"]

#                 index_path = index["path"]

#         # if not found_index: return None
#         schema = schema_builder.build()
#         index = tantivy.Index(schema, path=index_path)

#         if with_schema:
#             return index, fetched_schema

#         return index

#     def create(self, batch: bool = True):
#         if self._check_index_exists(self.name):
#             return self.get_index(self.name)

#         if not self.fields:
#             print(
#                 "Specify fields to index using the fields parameter i.e. create(name, fields=[])"
#             )
#             return None

#         index_path = self.db_path + "/full_text/" + self.name

#         index_specs = {"name": self.name, "schema": ["_id"], "path": index_path}

#         schema_builder = tantivy.SchemaBuilder()
#         schema_builder.add_text_field("_id", stored=True)

#         for field in self.fields:
#             schema_builder.add_text_field(field, stored=False)
#             index_specs["schema"].append(field)

#         schema = schema_builder.build()

#         self._create_dir(index_path)
#         self._add_index(index_specs)

#         index = tantivy.Index(schema, path=index_path)
#         writer = index.writer()

#         current_doc_id = ""
#         current_doc = {}

#         for key in self._iterate_keys():
#             decoded_key = encoding.decode_str(key).split("/")

#             doc_id = decoded_key[1]
#             key_column = decoded_key[2]

#             if doc_id != current_doc_id:
#                 if current_doc:
#                     # append doc to index
#                     current_doc["_id"] = [current_doc_id]
#                     writer.add_document(tantivy.Document(**current_doc))
#                     print(current_doc)
#                     if not batch:
#                         writer.commit()

#                 current_doc = {}
#                 current_doc_id = doc_id

#             if key_column in self.fields:
#                 key_value = self._get(key)

#                 if key_value:
#                     current_doc[key_column] = [key_value]

#         if batch:
#             writer.commit()

#         return index

#     def search(self, query: str, fields=None, limit: int = 1):
#         results = []

#         index, schema_fields = self.get_index(self.name, True)
#         if not fields:
#             fields = schema_fields

#         index.reload()
#         searcher = index.searcher()
#         parsed_query = index.parse_query(query, fields)
#         text_results = searcher.search(parsed_query, limit).hits

#         for result in text_results:
#             score, address = result
#             document_id = searcher.doc(address)["_id"][0]

#             results.append(self.get(document_id))

#         return results

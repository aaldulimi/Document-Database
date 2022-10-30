from src.rocky import RockyDB
from tests.load import load


class TestTextSearch:
    def test_create_index(self):
        db = RockyDB("database/")
        news = db.collection("t1")

        i = 0
        for document in load("tests/data.xml"):
            news.insert(document.__dict__)
            i += 1
            if i == 20:
                break

        index = news.create_index("a1", fields=["title", "author", "body"], batch=True)
        result_doc = index.search(
            "percent the year before", fields=["title", "author", "body"], limit=10
        )[0]

        assert type(result_doc) == dict

    # def test_get_index(self):
    #     db = RockyDB("database/")
    #     news = db.collection("text_1")

    #     insert_doc = {"title": "Some random title", "year": 2022, "_id": "a1"}

    #     index = news.get_index("index2")
    #     result_doc = index.search("random", fields=["title"], limit=1)[0]

    #     del result_doc["_id"]
    #     del insert_doc["_id"]

    #     assert result_doc == insert_doc

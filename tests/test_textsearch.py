from src.rocky import RockyDB


class TestTextSearch:
    def test_create_index(self):
        db = RockyDB("database/")
        news = db.collection("news_test")

        insert_doc = {"title": "Some random title", "year": 2022, "_id": "a1"}

        for _ in range(50):
            news.insert(insert_doc)

        index = news.create_index("index2", fields=["title"])
        result_doc = index.search("random", fields=["title"], limit=1)[0]

        del result_doc["_id"]
        del insert_doc["_id"]

        assert result_doc == insert_doc

    def test_get_index(self):
        db = RockyDB("database/")
        news = db.collection("news_test")

        insert_doc = {"title": "Some random title", "year": 2022, "_id": "a1"}

        index = news.get_index("index2")
        result_doc = index.search("random", fields=["title"], limit=1)[0]

        del result_doc["_id"]
        del insert_doc["_id"]

        assert result_doc == insert_doc

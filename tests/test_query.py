from src.rocky import RockyDB


class TestQuery:
    def test_query(self):
        db = RockyDB("database/")
        news = db.collection("news")

        insert_doc = {"title": "Some random title", "year": 2022, "_id": "a1"}

        news.insert(insert_doc)

        query_doc = news.find({"title": "Some random title"}, limit=1)[0]

        assert query_doc == insert_doc

    def test_empty_query(self):
        db = RockyDB("database/")
        news = db.collection("news")

        insert_doc = {"title": "Some random title", "year": 2022, "_id": "a1"}

        news.insert(insert_doc)

        results = news.find({"title": "no"}, limit=1)

        assert results == []

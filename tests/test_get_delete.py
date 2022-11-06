from rockydb import RockyDB


class TestGetDelete:
    def test_get(self):
        db = RockyDB("database/")
        news = db.collection("get_1")

        insert_doc = {"title": "Some random title", "year": 2022, "_id": "a1"}

        news.insert(insert_doc)

        get_doc = news.get("a1")

        assert insert_doc == get_doc

    def test_delete(self):
        db = RockyDB("database/")
        news = db.collection("delete_1")

        insert_doc = {"title": "Some random title", "year": 2022, "_id": "a1"}

        news.insert(insert_doc)
        get_doc = news.get("a1")

        assert insert_doc == get_doc

        news.delete("a1")
        get_doc = news.get("a1")

        assert get_doc == None

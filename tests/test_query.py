from rockydb import RockyDB


class TestQuery:
    def test_query(self):
        db = RockyDB("database/")
        news = db.collection("q1")

        insert_doc = {"title": "Some random title", "year": 2022, "_id": "a1"}

        news.insert(insert_doc)

        query_doc = news.find({"title": "Some random title"}, limit=1)[0]

        assert query_doc == insert_doc

    def test_empty_query(self):
        db = RockyDB("database/")
        news = db.collection("q2")

        insert_doc = {"title": "Some random title", "year": 2022, "_id": "a1"}

        news.insert(insert_doc)

        results = news.find({"title": "no"}, limit=1)

        assert results == []

    def test_adv_query(self):
        db = RockyDB("database/")
        db.clean_up()
        news = db.collection("q3")

        for i in range(50):
            news.insert({"number": i, "title": "something here"})

        lt = news.find({"number?lt": 25}, limit=100)
        lte = news.find({"number?lte": 25}, limit=100)
        gt = news.find({"number?gt": 10}, limit=100)
        gte = news.find({"number?gte": 10}, limit=100)

        assert len(lt) == 25
        assert len(lte) == 26
        assert len(gt) == 39
        assert len(gte) == 40

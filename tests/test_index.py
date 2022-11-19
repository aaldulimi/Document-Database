from rockydb import RockyDB
import random


class TestIndex:
    def test_creation(self):
        db = RockyDB("database/")
        index_test = db.collection("index_test")

        for _ in range(120):
            rand_int = random.randrange(1, 100)
            index_test.insert(
                {"number": rand_int, "name": "something", "arr": [1, 2, 3, 4, 5]}
            )

        index = index_test.create_index("test_index", field="number")
        assert index.key_count == 120

    def test_lte(self):
        db = RockyDB("database/")
        index_test = db.collection("index_lte_test")

        for _ in range(120):
            rand_int = random.randrange(1, 100)
            index_test.insert(
                {"number": rand_int, "name": "something", "arr": [1, 2, 3, 4, 5]}
            )

        index = index_test.create_index("test_index", field="number")
        results = index.find({"number?lte": 50})

        for doc_id in results:
            doc = index_test.get(doc_id)
            assert doc["number"] <= 50

    def test_lt(self):
        db = RockyDB("database/")
        index_test = db.collection("index_lt_test")

        for _ in range(120):
            rand_int = random.randrange(1, 100)
            index_test.insert(
                {"number": rand_int, "name": "something", "arr": [1, 2, 3, 4, 5]}
            )

        index = index_test.create_index("test_index", field="number")
        results = index.find({"number?lt": 50})

        for doc_id in results:
            doc = index_test.get(doc_id)
            assert doc["number"] < 50

    def test_gt(self):
        db = RockyDB("database/")
        index_test = db.collection("index_gt_test")

        for _ in range(120):
            rand_int = random.randrange(1, 100)
            index_test.insert(
                {"number": rand_int, "name": "something", "arr": [1, 2, 3, 4, 5]}
            )

        index = index_test.create_index("test_index", field="number")
        results = index.find({"number?gt": 50})

        for doc_id in results:
            doc = index_test.get(doc_id)
            assert doc["number"] > 50

    def test_gte(self):
        db = RockyDB("database/")
        index_test = db.collection("index_gte_test")

        for _ in range(120):
            rand_int = random.randrange(1, 100)
            index_test.insert(
                {"number": rand_int, "name": "something", "arr": [1, 2, 3, 4, 5]}
            )

        index = index_test.create_index("test_index", field="number")
        results = index.find({"number?gte": 50})

        for doc_id in results:
            doc = index_test.get(doc_id)
            assert doc["number"] >= 50

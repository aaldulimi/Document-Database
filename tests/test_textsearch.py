from src.paper import PaperDB


class TestQuery:
    def test_query(self):
        db = PaperDB('database/')
        news = db.collection('news_test')

        insert_doc = {
            "title": "Some random title",
            "year": 2022,
            "_id": "a1"
        }
        
        news.insert(insert_doc)

        index = news.get_index("simple_index")
        result_doc = index.search("Some", fields=["title"], limit=1)
        
        assert result_doc == insert_doc
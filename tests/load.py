import dataclasses
from lxml import etree


@dataclasses.dataclass
class Document:
    _id: str
    title: str
    author: str
    body: str
    url: str


def load(file_location):
    with open(file_location, "rb") as file:
        article_count = 1
        for _, doc in etree.iterparse(file, events=("end",), tag="doc"):
            title = doc.findtext("./title")
            author = doc.findtext("./author")
            body = doc.findtext("./body")
            url = doc.findtext("./url")

            yield Document(
                _id=str(article_count), title=title, author=author, body=body, url=url
            )
            article_count += 1
            doc.clear()

import dataclasses


@dataclasses.dataclass
class Document:
    title: str
    author: str
    body: str

class Subscriber:
    def __init__(self, id, chat_id, first_name, last_name):
        self.id = id
        self.chat_id = chat_id
        self.first_name = first_name
        self.last_name = last_name

    def __str__(self) -> str:
        return f"Subscriber(id={self.id}, chat_id={self.chat_id}, first_name={self.first_name}, last_name={self.last_name})"

class Article:
    def __init__(self, title: str, link: str, rank: int, score: int):
        self.title = title
        self.link = link
        self.rank = rank
        self.score = score

    def __repr__(self) -> str:
        return f"Article(title={self.title}, link={self.link}, rank={self.rank}, score={self.score})"
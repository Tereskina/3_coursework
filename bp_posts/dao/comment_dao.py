import json
from json import JSONDecodeError

from bp_posts.dao.comment import Comment
from exeptions.data_exceptions import DataSourceError


class CommentDAO:

    def __init__(self, path):
        self.path = path

    def _load_data(self):
        """
        Загружает данные из JSON, возвращает список словарей
        """

        try:
            with open(self.path, 'r', encoding='utf-8') as file:
                comments_data = json.load(file)
        except(FileNotFoundError, JSONDecodeError):
            raise DataSourceError(f"Не удаётся получить данные из файла {self.path}")
        return comments_data

    def _load_comments(self):
        """
        Возвращает список экземпляров Comment
        """

        comments_data = self._load_data()

        # list_of_posts = [Comment(**comment_data) for comment_data in comments_data]
        # распаковка именованных аргументов =
        # for one_comment in comment_data:
        #     Comment(
        #         post_id=one_comment["pk"],
        #         commenter_name=one_comment["commenter_name"],
        #         comment=one_comment["comment"],
        #         pk=one_comment["pk"]
        #     )
        comments = [Comment(**comment_data) for comment_data in comments_data]
        return comments

    def get_comments_by_post_id(self, post_id: int) -> list[Comment]:
        """
        Получает все комментарии к определённому посту по его id
        """
        comments: list[Comment] = self._load_comments()
        comments_match: list[Comment] = [c for c in comments if c.post_id == post_id]

        return comments_match


# cd = CommentDAO("../../data/comments.json")


# print(cd._load_comments())
# print(cd.get_comments_by_post_id(2))

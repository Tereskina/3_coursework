import pytest

from bp_posts.dao.comment import Comment
from bp_posts.dao.comment_dao import CommentDAO



def check_fields(comment):

    fields = ["post_id", "commenter_name", "comment", "pk"]

    for field in fields:
        assert hasattr(comment, field), f"Нет поля {field}"


class TestCommentsDAO:

    @pytest.fixture()
    def comment_dao(self):
        comment_dao_instance = CommentDAO('bp_posts/tests/comment_mock.json')
        return comment_dao_instance

    ### Функция получения комментариев к определённому посту

    def test_comments_by_post_id(self, comment_dao):

        comments = comment_dao.get_comments_by_post_id(1)
        assert type(comments) == list, "Incorrect type for list of comments"

        for comment in comments:
            assert type(comment) == Comment, "Incorrect type for single post"

    def test_comments_by_post_id_fields(self, comment_dao):
        comments = comment_dao.get_comments_by_post_id(1)
        for comment in comments:
            check_fields(comment)

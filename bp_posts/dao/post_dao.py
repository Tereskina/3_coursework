import json
import re
from json import JSONDecodeError
from pprint import pprint as pp
from bp_posts.dao.post import Post
from exeptions.data_exceptions import DataSourceError


class PostDAO:
    """
    Менеджер абстракции post.py. Менеджер постов: загружает, показывает, ищет по pk и пользователю
    """

    def __init__(self, path):
        self.path = path


    def _load_data(self) -> list[dict]:
        """
        Загружает данные из JSON, возвращает список словарей
        """

        try:
            with open(self.path, 'r', encoding='utf-8') as file:
                posts_data = json.load(file)
        except(FileNotFoundError, JSONDecodeError):
            raise DataSourceError(f"Не удаётся получить данные из файла {self.path}")
        return posts_data


    def _load_posts(self) -> list[Post]:
        """
        Возвращает список экземпляров POST
        """

        posts_data = self._load_data()

        list_of_posts = [Post(**post_data) for post_data in posts_data]
        # распаковка именованных аргументов =
        # = Post(poster_name = post_data["poster_name"]итд
        return list_of_posts


    def get_all(self) -> list[Post]:
        """
        Получаем все посты, возвращает список экземпляров класса Post
        """
        posts = self._load_posts()
        return posts

    def get_by_pk(self, pk) -> Post:
        """
        Получает пост по его pk
        """
        if type(pk) != int:
            raise TypeError('pk must be an int')

        posts = self._load_posts()
        for post in posts:
            if post.pk == pk:
                return post


    def search_in_content(self, substring) -> list[Post] | None:
        """
        Ищет посты, где в контенте встречается substring
        """
        if type(substring) != str:
            raise TypeError('substring must be an str')

        substring = substring.lower()
        posts = self._load_posts()

        matching_posts = [post for post in posts if substring in post.content.lower()]

        return matching_posts

    def get_by_poster(self, user_name) -> list[Post] | None:
        """
        Ищем посты с определённым автором
        """
        if type(user_name) != str:
            raise TypeError('user_name must be an str')
        user_name = user_name.lower()
        posts = self._load_posts()


        matching_posts = [post for post in posts if post.poster_name.lower() == user_name]

        return matching_posts

    def tag_replace(self, post_pk):
        """
        Просматривает пост
        """
        post = self.get_by_pk(post_pk)
        words = post.content.split()
        content_with_links = []

        for word in words:
            if word.startswith("#"):
                content_with_links.append(f'<a href="/tag/{word[1:]}/">{word}</a>')
            else:
                content_with_links.append(word)


        post.content = " ".join(content_with_links)
        return post

    def tag_names(self, tag_name):
        """
        Возвращает посты с тэгами
        """
        tag = []
        for tag_post in self.search_in_content(tag_name):
            if re.search(tag_name + " ", tag_post.content):
                tag.append(tag_post)
        return tag











# проверка
# pd = PostDAO("../../data/data.json")
# pp(pd)
# pp(pd._load_data())
# pp(pd._load_posts())
# pp(pd.get_by_pk(2))
# pp(pd.search_in_content("елки"))
# pp(pd.get_by_poster("LARRY"))

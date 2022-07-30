import json
from json import JSONDecodeError
from pprint import pprint as pp
from bp_posts.dao.bookmark import Bookmark
from bp_posts.dao.post_dao import PostDAO

from exeptions.data_exceptions import DataSourceError




class BookmarkDAO:
    """
    Менеджер абстракции post.py. Менеджер постов: загружает, показывает, ищет по pk и пользователю
    """

    def __init__(self, path, post_dao):
        self.path = path
        self.post_dao = post_dao


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


    def get_by_pk(self, pk) -> Bookmark:
        """
        Получает пост по его pk
        """
        if type(pk) != int:
            raise TypeError('pk must be an int')

        posts = self._load_posts()

        for post in posts:
            if post.pk == pk:
                return post

    def _load_posts(self) -> list[Bookmark]:
        """
        Возвращает список экземпляров POST
        """

        posts_data = self._load_data()

        list_of_posts = [Bookmark(**post_data) for post_data in posts_data]
        # распаковка именованных аргументов =
        # = Bookmark(poster_name = post_data["poster_name"]итд
        return list_of_posts


    def get_all(self) -> list[Bookmark]:
        """
        Получаем все посты, возвращает список экземпляров класса Post
        """
        posts = self._load_posts()
        return posts

    def add_bookmark(self, pk: int) -> None:
        """
        Добавляет закладку
        """
        bookmarks_list: list[dict] = self._load_data()
        bookmarks_list_obj: list[Bookmark] = self._load_posts()
        post = self.post_dao.get_by_pk(pk)

        new_bookmark = Bookmark(
            pk=pk,
            poster_name=post.poster_name,
            poster_avatar=post.poster_avatar,
            pic=post.pic,
            content=post.content,
            views_count=post.views_count,
            likes_count=post.likes_count
        )

        bookmark_exist = False

        for bookmark_post in bookmarks_list_obj:
            if new_bookmark.pk == bookmark_post.pk:
                bookmark_exist = True


        if not bookmark_exist:
            bookmarks_list.append(new_bookmark.as_dict())
            # print("bookmarks_list")
            # pp(bookmarks_list)
            with open(self.path, "w", encoding='utf-8') as file:
                json.dump(bookmarks_list, file, ensure_ascii=False)
        else:
            print("Пост уже был добавлен, или нет такого pk")


    def remove_bookmark(self, pk):
        """
        Удаляет закладку
        """
        bookmarks_list: list[dict] = self._load_data()
        bookmarks_list_obj: list[Bookmark] = self._load_posts()
        post = self.post_dao.get_by_pk(pk)

        for bookmark_post in bookmarks_list_obj:
            if post.pk == bookmark_post.pk:
                bookmarks_list.remove(post.as_dict())
                pp(bookmarks_list)
                with open(self.path, "w", encoding='utf-8') as file:
                    json.dump(bookmarks_list, file, ensure_ascii=False)
            else:
                "Невозможно удалить"



# # #
# t = PostDAO("../../data/data.json")
# b = BookmarkDAO("../../data/bookmarks.json", t)
# #
# pp(b.remove_bookmark(4))
# # # #
# # print(b._load_data())
# # print(b._load_posts())
# pp(b.add_bookmark(4))
# # print(b.get_all_bookmarks())
# # print(b.add_bookmark(4))
# # print(b.get_all_bookmarks())


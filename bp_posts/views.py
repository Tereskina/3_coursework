from flask import Blueprint, render_template, request, redirect
from werkzeug.exceptions import abort

from bp_posts.dao import bookmark_dao

from bp_posts.dao.bookmark_dao import BookmarkDAO
from bp_posts.dao.post_dao import PostDAO
from bp_posts.dao.comment_dao import CommentDAO



from bp_posts.dao.post import Post




from config import DATA_PATH_POSTS, DATA_PATH_COMMENTS, DATA_PATH_BOOKMARKS

bp_posts = Blueprint("bp_posts", __name__, template_folder="templates")

# Создаём объекты доступа к данным
post_dao = PostDAO(DATA_PATH_POSTS)
comment_dao = CommentDAO(DATA_PATH_COMMENTS)
bookmark_dao = BookmarkDAO(DATA_PATH_BOOKMARKS, post_dao)



@bp_posts.route('/')
def page_posts_index():
    """Страничка всех постов"""
    all_posts = post_dao.get_all()
    return render_template("index.html", posts=all_posts)


@bp_posts.route('/posts/<int:pk>/')
def page_post_single(pk: int):
    """Страничка одного поста"""
    post = post_dao.tag_replace(pk)
    comments = comment_dao.get_comments_by_post_id(pk)
    comments_len = len(comments)

    if post is None:
        abort(404)

    return render_template("post.html",
                           post=post,
                           comments=comments,
                           comments_len=comments_len
                           )


@bp_posts.route("/users/<poster_name>")
def page_posts_by_poster(poster_name: str):
    """Возвращает посты пользователя"""
    posts: list[Post] = post_dao.get_by_poster(poster_name)

    if not posts:
        abort(404, "Такого пользователя не существует")

    return render_template('user-feed.html',
                           posts=posts,
                           poster_name=poster_name
                           )


@bp_posts.route("/search/")
def page_posts_search():
    """Возвращает результаты поиска"""

    query: str = request.args.get("s", "")

    if query == "":
        posts: list = []
    else:
        posts: list[Post] = post_dao.search_in_content(query)

    return render_template("search.html",
                           posts=posts,
                           query=query,
                           posts_len=len(posts),
                           )


@bp_posts.route("/tag/<tag_name>/")
def page_tag(tag_name: str):
    """ Реализует переход по тегам"""
    posts = post_dao.search_in_content("#" + tag_name)
    tag_names = post_dao.tag_names(tag_name)
    if not posts:
        abort(404, "Такого тега не существует")

    for post in posts:
        if tag_name in post.content:
            return render_template("tag.html", tag_names=tag_names, search_tag=tag_name)


@bp_posts.route('/bookmarks/add/<int:pk>/')
def page_bookmark_add(pk: int):
    """Добавление в закладки одного поста"""
    bookmark_dao.add_bookmark(pk)

    return redirect("/", code=302)


@bp_posts.route('/bookmarks/remove/<int:pk>/')
def page_bookmark_remove(pk: int):
    """Удаление поста из закладок"""
    bookmark_dao.remove_bookmark(pk)

    return redirect("/", code=302)


@bp_posts.route('/bookmarks/')
def page_bookmark_all():
    """Страничка всех закладок"""
    bookmarks = bookmark_dao.get_all()
    return render_template("bookmarks.html", bookmarks=bookmarks)

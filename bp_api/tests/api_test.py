import os.path

import pytest

import main


class TestApi:

    post_keys = {"poster_name", "poster_avatar", "pic", "content", "views_count", "likes_count", "pk"}


    @pytest.fixture
    def app_instance(self):
        app = main.app
        app.config["DATA_PATH_POSTS"] = os.path.join("bp_posts", "tests", "post_mock")
        test_client = app.test_client()
        return test_client

    def test_all_posts_have_correct_status(self, app_instance):
        result = app_instance.get("/api/posts", follow_redirects=True)
        # print(result.data)
        assert result.status_code == 200

    def test_all_posts_have_correct_keys(self, app_instance):
        result = app_instance.get("/api/posts", follow_redirects=True)
        list_of_posts = result.get_json()
        for post in list_of_posts:
            assert post.keys() == self.post_keys, "Неправильные ключи у словаря"


    # single_post


    def test_single_post_has_correct_status(self, app_instance):
        result = app_instance.get("/api/posts/1", follow_redirects=True)
        assert result.status_code == 200, "Неправильный "

    def test_single_post_non_exists_shows_404(self, app_instance):
        result = app_instance.get("/api/posts/0", follow_redirects=True)
        assert result.status_code == 404

    def test_single_post_has_correct_keys(self, app_instance):
        result = app_instance.get("/api/posts/1", follow_redirects=True)
        post = result.get_json()
        post_keys = set(post.keys())
        assert post_keys == self.post_keys, "Неправильный ключи у полученного словаря"

    @pytest.mark.parametrize("pk", [1, 2, 3, 4])
    def test_single_post_has_correct_data(self, app_instance, pk):
        result = app_instance.get(f"/api/posts/{pk}", follow_redirects=True)
        post = result.get_json()
        assert post["pk"] == pk, f"Неправильный зл при запросе поста {pk}"






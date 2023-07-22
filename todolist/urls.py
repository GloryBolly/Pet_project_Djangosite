from django.urls import path

from .views import *

urlpatterns = [
    path("", ToDoListHome.as_view(), name="home"),
    path("about/", about, name="about"),
    path("create/", AddSnippet.as_view(), name="create"),
    path("delete/", delete_snippet, name="delete"),
    path("login/", login, name="login"),
    path("post/<slug:post_slug>/", ShowPost.as_view(), name="post"),
    path("category/<slug:cat_slug>/", ToDoListCategory.as_view(), name="category"),
]

from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("search/", views.search, name="search"),
    path("add/", views.add, name="add"),
    path("note/<pk>", views.note, name="note"),
    path("delete/<int:note_id>", views.delete_note, name="delete"),
    path("download/<int:note_id>", views.download_note, name="download"),
    path("duplicate/<int:note_id>", views.duplicate_note, name="duplicate"),
    path("about/", views.about, name="about"),
    path("account/", views.account, name="account"),
]

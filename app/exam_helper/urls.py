from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("trial", views.trial, name="trial"),
    path("options", views.options, name="options"),
    path("summary", views.summary, name="summary"),
    path("quiz", views.quiz, name="quiz"),
    path("flashcard", views.flashcard, name="flashcard"),
    path("podcast", views.podcast, name="podcast"),
]
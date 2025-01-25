from django.urls import path
from characters import views

urlpatterns = [
    path("", views.index, name="characters-index"),
]

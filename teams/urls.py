from django.urls import path
from teams import views

urlpatterns = [
    path("", views.index, name="teams-index"),
]

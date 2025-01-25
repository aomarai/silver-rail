from django.urls import path
from lightcones import views

urlpatterns = [
    path("", views.index, name="lightcones-index"),
]

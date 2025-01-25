from django.urls import path
from abilities import views

urlpatterns = [
    path("", views.index, name="abilities-index"),
]

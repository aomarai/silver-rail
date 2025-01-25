from django.urls import path
from relics import views

urlpatterns = [
    path('', views.index, name='relics-index'),
]
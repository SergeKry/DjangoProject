from django.urls import path

from . import views

app_name = 'members_app'
urlpatterns = [
    path("", views.index, name="index"),
    path("results/", views.results, name="results"),
    path("save_input/", views.save_input, name="save_input"),
]
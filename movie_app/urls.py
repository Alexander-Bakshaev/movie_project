from . import views
from django.urls import path, include

urlpatterns = [
    path('', views.sow_all_movies),
    path('movie/<slug:slug_movie>', views.show_one_movie, name='movie-detail'),
]

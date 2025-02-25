from . import views
from django.urls import path, include

urlpatterns = [
    path('', views.sow_all_movies),
]

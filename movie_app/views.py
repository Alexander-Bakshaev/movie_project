from django.shortcuts import render

from .models import Movie


def sow_all_movies(request):
    movies = Movie.objects.all()
    return render(request, 'movie_app/all_movies.html', {'movies': movies})

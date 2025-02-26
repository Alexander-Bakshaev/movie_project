from tkinter.font import names

from django.shortcuts import render, get_object_or_404
from .models import Movie


def sow_all_movies(request):
    movies = Movie.objects.order_by('name')[:3]
    return render(request, 'movie_app/all_movies.html', {'movies': movies})


def show_one_movie(request, slug_movie: str):
    movie = get_object_or_404(Movie, slug=slug_movie)
    return render(request, 'movie_app/one_movie.html', {'movie': movie})

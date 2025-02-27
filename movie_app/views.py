from tkinter.font import names
from django.db.models import F, Max, Min, Avg, Sum, Count, Value
from django.shortcuts import render, get_object_or_404
from .models import Movie


def sow_all_movies(request):
    # movies = Movie.objects.order_by(F('rating').desc(nulls_last=True))
    movies = Movie.objects.annotate(
        true_bool=Value(True),
        false_str=Value('Hello'),
        new_budget=F('budget') * 2,
        new_raing=F('rating') * F('budget')
    )
    agg = movies.aggregate(Avg('budget'), Max('rating'), Min('rating'), Count('id'))
    return render(request, 'movie_app/all_movies.html', {
        'agg': agg,
        'movies': movies
    })


def show_one_movie(request, slug_movie: str):
    movie = get_object_or_404(Movie, slug=slug_movie)
    return render(request, 'movie_app/one_movie.html', {'movie': movie})

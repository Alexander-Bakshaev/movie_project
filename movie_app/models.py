from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from transliterate import translit
from django.core.validators import MinValueValidator, MaxValueValidator


class Movie(models.Model):
    EUR = 'EUR'
    USD = 'USD'
    RUB = 'RUB'
    CURRENCY_CHOICES = [
        (EUR, 'Euro'),
        (USD, 'Dollar'),
        (RUB, 'Rubles'),
    ]

    name = models.CharField(max_length=50, verbose_name='Название')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)], verbose_name='Рейтинг')
    year = models.IntegerField(null=True, blank=True)
    budget = models.IntegerField(default=1000000, blank=True, validators=[MinValueValidator(1)], verbose_name='Бюджет')
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default=RUB, verbose_name='Валюта')
    slug = models.SlugField(default='', null=False, db_index=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(translit(self.name, 'ru', reversed=True))
        super().save(*args, **kwargs)

    def get_url(self):
        return reverse('movie-detail', args=[self.slug])

    def __str__(self):
        return f'{self.name} - {self.rating}%'

    class Meta:
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['slug'], name='slug_idx'),
        ]

# from movie_app.models import Movie

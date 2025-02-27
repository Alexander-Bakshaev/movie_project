from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from transliterate import translit

class Movie(models.Model):
    name = models.CharField(max_length=50)
    rating = models.IntegerField()
    year = models.IntegerField(null=True)
    budget = models.IntegerField(default=1000000)
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

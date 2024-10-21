from django.db import models
import random
from django.contrib.auth.models import User


class Director(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    duration = models.IntegerField()
    director = models.ForeignKey(Director, on_delete=models.CASCADE, related_name='movies')

    def __str__(self):
        return self.title


class Review(models.Model):
    text = models.TextField()
    stars = models.IntegerField(default=1)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')

    def __str__(self):
        return f'{self.movie.title} - {self.stars} stars'


class ConfirmationCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='confirmation_code')
    code = models.CharField(max_length=6)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = str(random.randint(100000, 999999))  # Генерация 6-значного кода
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Code for {self.user.username}: {self.code}"

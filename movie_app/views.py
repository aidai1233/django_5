from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Avg
from rest_framework import generics
from .models import Director, Movie, Review
from .serializers import DirectorSerializer, MovieSerializer, ReviewSerializer, MovieWithReviewsSerializer


class DirectorList(generics.ListCreateAPIView):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer


class DirectorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer


class MovieList(generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class MovieDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class ReviewList(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class MoviesWithReviews(APIView):
    def get(self, request):
        movies = Movie.objects.prefetch_related('reviews').all()
        for movie in movies:
            movie.avg_rating = movie.reviews.aggregate(Avg('stars'))['stars__avg']
        serializer = MovieWithReviewsSerializer(movies, many=True)
        return Response(serializer.data)


class DirectorsWithMoviesCount(APIView):
    def get(self, request):
        directors = Director.objects.annotate(movies_count=Count('movies'))
        serializer = DirectorSerializer(directors, many=True)
        return Response(serializer.data)
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Avg
from rest_framework import generics, status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .models import Director, Movie, Review, ConfirmationCode
from .serializers import (
    DirectorSerializer, MovieSerializer, ReviewSerializer, MovieWithReviewsSerializer, RegisterSerializer,
    ConfirmUserSerializer
)

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


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "Пользователь создан. Проверьте email для получения кода подтверждения."},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConfirmUserView(APIView):
    def post(self, request):
        serializer = ConfirmUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Пользователь подтвержден и активирован."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                token, created = Token.objects.get_or_create(user=user)
                return Response({"token": token.key})
            return Response({"error": "Неправильный пароль."}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"error": "Пользователь не найден."}, status=status.HTTP_400_BAD_REQUEST)
from rest_framework import serializers
from .models import Director, Movie, Review


class DirectorSerializer(serializers.ModelSerializer):
    movies_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Director
        fields = ['id', 'name', 'movies_count']


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class MovieWithReviewsSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    avg_rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Movie
        fields = ['id', 'title', 'description', 'duration', 'reviews', 'avg_rating']
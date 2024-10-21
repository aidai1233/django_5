from rest_framework import serializers
from .models import Director, Movie, Review, ConfirmationCode
from django.contrib.auth.models import User


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = '__all__'

    def validate_name(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Имя режиссера должно содержать не менее 3 символов.")
        return value


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

    def validate_duration(self, value):
        if value <= 0:
            raise serializers.ValidationError("Продолжительность фильма должна быть положительной.")
        return value


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

    def validate_stars(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Рейтинг отзыва должен быть в диапазоне от 1 до 5.")
        return value


class MovieWithReviewsSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    avg_rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Movie
        fields = ['id', 'title', 'description', 'duration', 'reviews', 'avg_rating']


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            is_active=False
        )

        ConfirmationCode.objects.create(user=user)
        return user


class ConfirmUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    code = serializers.CharField(max_length=6)

    def validate(self, data):
        try:
            user = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            raise serializers.ValidationError("Пользователь не найден.")

        if user.confirmation_code.code != data['code']:
            raise serializers.ValidationError("Неверный код подтверждения.")

        return data

    def save(self):
        user = User.objects.get(username=self.validated_data['username'])
        user.is_active = True
        user.save()
        user.confirmation_code.delete()
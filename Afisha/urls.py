"""
URL configuration for Afisha project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from movie_app.views import (
    DirectorList,
    DirectorDetail,
    MovieList,
    MovieDetail,
    ReviewList,
    ReviewDetail,
    MoviesWithReviews,
    DirectorsWithMoviesCount,
    RegisterView,
    ConfirmUserView,
    LoginView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/directors/', DirectorList.as_view(), name='director-list'),
    path('api/v1/directors/<int:id>/', DirectorDetail.as_view(), name='director-detail'),
    path('api/v1/movies/', MovieList.as_view(), name='movie-list'),
    path('api/v1/movies/<int:id>/', MovieDetail.as_view(), name='movie-detail'),
    path('api/v1/reviews/', ReviewList.as_view(), name='review-list'),
    path('api/v1/reviews/<int:id>/', ReviewDetail.as_view(), name='review-detail'),
    path('api/v1/movies/reviews/', MoviesWithReviews.as_view(), name='movies-with-reviews'),
    path('api/v1/directors/', DirectorsWithMoviesCount.as_view(), name='directors-with-movies-count'),
    path('api/v1/users/register/', RegisterView.as_view(), name='register'),
    path('api/v1/users/confirm/', ConfirmUserView.as_view(), name='confirm-user'),
    path('api/v1/users/login/', LoginView.as_view(), name='login'),

]



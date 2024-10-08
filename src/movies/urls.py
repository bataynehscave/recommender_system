from django.urls import path

from . import views

urlpatterns = [
    path('', views.movie_list_view),
    path('<int:pk>', views.movie_detail_view),
    path('infinite/', views.movie_infinte_rating_view),
]
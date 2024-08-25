from .models import Movie
from celery import shared_task

# @shared_task(name = 'task_calculate_movie_ratings')
# def task_calculate_movies_ratings(count:int = 1000) -> None:

#     '''
#     task_calculate_movie_ratings( count=None)
#     # celery tasks
#     task_calculate_movie_ratings.delay(count=None)
#     task_calculate_movie_ratings.apply_async(kwargs = {
#      "count":12}, countdown = 30)
#     '''

#     qs = Movie.objects.all()
#     qs.order_by('rating_last_updated')
#     if isinstance(count, int):
#         qs = qs[:count]
#     for obj in qs:
#         obj.calculate_rating(save=True)
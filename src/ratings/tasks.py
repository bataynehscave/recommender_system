from datetime import datetime
import random 
from movies.models import Movie
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from .models import Rating, RatingChoice
from celery import shared_task
from django.db.models import Avg, Count

@shared_task(name='generate_fake_reviews')
def generate_fake_reviews(count = 100, users=10, zero_avg=False):
    user_s = User.objects.first()
    user_e = User.objects.last()

    random_user_ids = random.sample(range(user_s.id, user_e.id), users)
    users = User.objects.filter(id__in=random_user_ids)
    
    movies = Movie.objects.all().order_by('?')[:count]
    
    if zero_avg:
        movies = Movie.objects.filter(rating_avg=0).order_by('?')[:count]
    
    n_ratings = count
    rating_choices = [x for x in RatingChoice.values if x is not None]
    user_ratings = [random.choice(rating_choices) for _ in range (0, n_ratings)]
    new_ratings = []
    for i in range(n_ratings): 
        rating_obj = Rating.objects.create(
            content_object=random.choice(movies),
            value = user_ratings.pop(),
            user=random.choice(users)
        )
        new_ratings.append(rating_obj.id)

    return new_ratings

@shared_task(name='task_update_movie_ratings')
def task_update_movie_ratings():
    agg_ratings = Rating.objects.filter(content_type = ContentType.objects.get_for_model(Movie)).values('object_id').annotate(average=Avg('value'), count=Count('object_id'))
    for agg_rate in agg_ratings:
        mid = agg_rate['object_id']
        qs = Movie.objects.filter(id = mid )
        qs.update(
            rating_avg = agg_rate['average'],
            rating_count = agg_rate['count'],
            rating_last_updated = timezone.now(),
        )
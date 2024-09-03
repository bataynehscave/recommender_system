from celery import shared_task
from .utils import train_model, load_model
from profiles import utils as prof_utils
from movies.models import Movie
from django.apps import apps
from django.contrib.contenttypes.models import ContentType
@shared_task
def train_surprise_model_task():
    train_model()

@shared_task
def batch_user_prediction_task(user_ids=None, start_page = 0, offset=250, max_pages = 1000):
    model = load_model()
    end_page = start_page + offset
    if user_ids:
        recent_users_ids  = [user_ids]
    else:
        recent_users_ids = prof_utils.get_recent_users()
    movie_ids = Movie.objects.all().values_list('id', flat=True)[start_page:end_page]
    Suggestion = apps.get_model('suggestions', 'Suggestion')
    ctype = ContentType.objects.get(app_label='movies', model='movie')
    new_suggestions = []
    if model is not None:
        for u in recent_users_ids:
            for movie_id in movie_ids:
                pred = model.predict(uid=u, iid=movie_id).est
                # print(u, movie_id, pred)
                data = {
                    'user_id': u,
                    'object_id': movie_id,
                    'value': pred,
                    'content_type': ctype
                }
                new_suggestions.append(
                    Suggestion(**data)
                )
        Suggestion.objects.bulk_create(new_suggestions, ignore_conflicts=True)
    if end_page<max_pages:
        return batch_user_prediction_task(user_ids=1,start_page=end_page - 1)


def batch_update_user_predictions_task(user_ids=1, start_page = 0, offset=250, max_pages = 1000):
    batch_user_prediction_task(user_ids=user_ids, start_page = start_page, offset=offset, max_pages = max_pages)
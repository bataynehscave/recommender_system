from django.core.management.base import BaseCommand, CommandParser
# from movies.tasks import task_calculate_movies_ratings
from ratings.tasks import task_update_movie_ratings

class Command(BaseCommand):

    
    def handle(self, *args, **options):

        task_update_movie_ratings()
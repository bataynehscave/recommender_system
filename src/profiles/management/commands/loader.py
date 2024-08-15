from django.core.management.base import BaseCommand, CommandParser
from django.contrib.auth import get_user_model
from movies.models import Movie
from home import utils as home_utils
User = get_user_model()

class Command(BaseCommand):

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('count', nargs='?', type=int, default=10)
        parser.add_argument('--add-users', default=False, action='store_true')
        parser.add_argument('--show-total', action='store_true', default = False)
        parser.add_argument('--show-movies', action='store_true', default=False)
        

    def handle(self, *args, **options):
        count = options.get('count')
        show_movies = options.get('show_movies')
        add_users = options.get('add_users')
        if show_movies:
            movies = home_utils.get_movies_metadata(count)
            movies = [Movie(**x) for x in movies]
            Movie.objects.bulk_create(movies, ignore_conflicts=True)
            
        if add_users:
            show_total = options.get('show_total')
            profiles = home_utils.get_fake_profile(count)
            new_users = []
            for profile in profiles:
                user = User(**profile)
                try:
                    user.full_clean()
                    new_users.append(user)
                    
                except ValidationError as e:
                    print(f"Error with profile: {profile}, Error: {e}")
                
            
            if new_users:
                users_bulk = User.objects.bulk_create(new_users, ignore_conflicts = True)
                print(f"created {len(new_users)} new users ")
            else:
                print('there is no new users')
            
            if show_total:
                print(f"Total users: {User.objects.count()}")
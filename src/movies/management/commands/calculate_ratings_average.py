from django.core.management.base import BaseCommand, CommandParser
from movies.tasks import task_calculate_movies_ratings


class Command(BaseCommand):
    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('count',nargs='?' ,type=int, default=1000)
    
    def handle(self, *args, **options):
        count = options.get('count')
        task_calculate_movies_ratings(count)
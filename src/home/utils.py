from faker import Faker
import csv 
from django.conf import settings
from pprint import pprint
import datetime

MOVIE_METADATA_CSV = settings.DATA_DIR / 'movies_metadata.csv'

def validate_date(date: str) -> str:
    try:
        datetime.datetime.strptime(date)
        return date
    except:
        return None

def get_movies_metadata(limit = 10000):
    with open(MOVIE_METADATA_CSV, newline='') as f:
        data = csv.DictReader(f)
        movies = []
        for i, row in enumerate(data):
            _id = row.get('id')
            try:
                _id = int(_id)
            except:
                _id = None
            release_date = validate_date(row.get('release_date'))
            movie_data = {
                'id': _id,
                'title': row.get('title'),
                'overview': row.get('overview'),
                'release_date': release_date
            }
            movies.append(movie_data)
            if i + 1 >= limit:
                break
        print(f'added {len(movies)}')
        return movies
            
    




def get_fake_profile(count = 10):
    fake = Faker()
    user_data = []
    for _ in range(count):
        profile = fake.profile()
        data = {
            'username': profile.get('username'),
            'password': 'password',
            'email': profile.get('email'),
            'is_active': True
        }
        if 'name' in profile:
            fname, lname = profile.get('name').split()[:2]
            data['first_name'] = ''.join(fname)
            data['last_name'] = ''.join(lname)
        user_data.append(data)
    
    return user_data


from django.db.models import F 
from django.contrib.contenttypes.models import ContentType
import csv
import tempfile
from django.apps import apps
from ratings.models import Rating
from django.core.files.base import File
def generate_ratings_dataset():
    ctype = ContentType.objects.get(app_label='movies', model='movie')
    qs = Rating.objects.filter(active=True, content_type = ctype)
    qs = qs.annotate(userId = F('user_id'), movieId=F('object_id'), rating=F('value'))
    return qs.values('userId', 'movieId', 'rating')

def export_dataset():
    Export = apps.get_model('exports', 'Export')
    with tempfile.NamedTemporaryFile(mode='r+') as temp_f:
        dataset = generate_ratings_dataset()
        try:
            keys = dataset[0].keys()
        except:
            return 
        
        dict_writer = csv.DictWriter(temp_f, keys)
        dict_writer.writeheader()
        dict_writer.writerows(dataset)
        temp_f.seek(0)
        obj = Export.objects.create()
        obj.file.save('export.csv', File(temp_f))

        



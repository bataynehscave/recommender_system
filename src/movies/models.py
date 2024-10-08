from datetime import timedelta
from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.utils import timezone
from django.db.models import F, Sum, Case, When
from ratings.models import Rating

class MovieManager(models.Manager):
    def popular(self):
        return self.annotate(score = Sum(
         F('rating_avg') * F('rating_count'),
         output_field = models.FloatField()   
        )
        ).order_by('-score')
    
    def by_id_order(self, movie_pks=[]):
        qs = self.get_queryset().filter(id__in=movie_pks)
        maintain_order = Case(*[When(pk=pki, then=idx) for idx, pki in enumerate(movie_pks)])

        return qs.order_by(maintain_order)

class Movie(models.Model):
    title = models.CharField(max_length=120, unique=True)
    overview = models.TextField()
    release_date = models.DateField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    ratings = GenericRelation(Rating)
    rating_last_updated = models.DateTimeField(blank=True, null=True)
    rating_count = models.IntegerField(blank=True, null=True)
    rating_avg = models.DecimalField(decimal_places=2, max_digits=5, blank=True, default=0.00)
    score = models.FloatField( null=True)
    objects = MovieManager()
    def get_absolute_url(self):
        return f'{self.id}'

    def calculate_ratings_count(self):
        
        return self.ratings.filter(active=True).count()
    
    def calculate_ratings_avg(self):
        
        return self.ratings.filter(active=True).avg() or 0.0
    
    def rating_avg_display(self):
        now = timezone.now()
        
        if not self.rating_last_updated:
            return self.calculate_rating()
        
        if self.rating_last_updated > now - timedelta(minutes=5):
            return self.rating_avg
        
        return self.calculate_rating()
        
    def calculate_rating(self, save=True):
        
        rating_avg = self.calculate_ratings_avg()
        rating_count = self.calculate_ratings_count()
        
        
        self.rating_count = rating_count
        self.rating_avg = rating_avg
        self.rating_last_updated = timezone.now()
        
        if save:
            self.save()
        
        return self.rating_avg
    
    def __str__(self) -> str:
        return f"{self.id}. {self.title}"

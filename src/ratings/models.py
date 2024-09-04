from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.apps.registry import apps
from django.utils import timezone
# Create your models here.

class RatingChoice(models.IntegerChoices):
    one = 1
    two = 2
    three = 3
    four = 4
    five = 5
    __empty__ = "choose value"

class RatingQuerySet(models.QuerySet):
    def avg(self):
        return self.aggregate(average=Avg('value'))['average']
    
    def movies(self):
        Movie = apps.get_model('movies', 'Movie')
        ctype = ContentType.objects.get_for_model(Movie)
        return self.filter(active=True, ContentType=ctype)
                              
class RatingManager(models.Manager):
    def get_queryset(self):
        return RatingQuerySet(self.model, using=self._db)

    def movies(self):
        return self.get_queryset().movies()
    
    def avg(self):
        return self.get_queryset().avg()


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.IntegerField(null=True, blank=True, choices=RatingChoice.choices)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    active_update_timestamp = models.DateTimeField(auto_now_add=False, auto_now=False, null=True, blank=True)

    objects = RatingManager()

    class Meta():
        ordering = ['-timestamp']


def rating_post_save(sender, instance, created, *args, **kwargs):
    if created:
        Suggestion = apps.get_model('suggestions','Suggestion')

        _id = instance.id
        if instance.active:
            qs = Rating.objects.filter(content_type=instance.content_type,
                                       object_id=instance.object_id,
                                       user=instance.user,
                                       active=True).exclude(id=_id)
            if qs.exists():
                qs.update(active=False)

            suggestion_qs = Suggestion.objects.filter(content_type=instance.content_type,
                                       object_id=instance.object_id,
                                       user=instance.user,
                                       did_rate=False).exclude(id=_id)
            if suggestion_qs.exists():
                suggestion_qs.update(
                    did_rate = True,
                    did_rate_timestamp=timezone.now(),
                    value = instance.value
                )

post_save.connect(rating_post_save, sender=Rating)


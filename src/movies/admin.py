from django.contrib import admin
from movies.models import Movie
# Register your models here.
class MovieAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'calculate_ratings_count']
    readonly_fields = ['calculate_ratings_count', 'calculate_ratings_avg']
admin.site.register(Movie, MovieAdmin)
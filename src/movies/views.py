from typing import Any
from django.shortcuts import render
from django.views import generic
# Create your views here.
from .models import Movie

class MovieListView(generic.ListView):
    template_name = 'movies/list.html'
    paginate_by = 100
    queryset = Movie.objects.all().order_by('-score')
    # qs = queryset.popular()

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        request = self.request
        user = request.user
        if user.is_authenticated:
            object_list = context['object_list']
            object_ids = [x.id for x in object_list]
            qs = user.rating_set.filter(object_id__in = object_ids, active=True)
            context['my_ratings'] = {f'{x.object_id}': x.value for x in qs}

        return context

movie_list_view = MovieListView.as_view()

class MovieDetailView(generic.DetailView):
    template_name = 'movies/detail.html'
    queryset = Movie.objects.all()

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        request = self.request
        user = request.user
        if user.is_authenticated:
            object = context['object']
            object_id = [object.id]
            qs = user.rating_set.filter(object_id__in = object_id, active=True)
            context['my_ratings'] = {f'{x.object_id}': x.value for x in qs}

        return context

movie_detail_view = MovieDetailView.as_view()

import random
class MovieInfiniteRatingView(MovieDetailView):
    def get_object(self):
        qs =  Movie.objects.all().order_by('-score')
        return random.choice(qs[:100])
    
    def get_template_names(self):
        request = self.request
        if request.htmx:
            return ['movies/snippet/infinite.html']
        return ['movies/infinite-view.html']

movie_infinte_rating_view = MovieInfiniteRatingView.as_view()
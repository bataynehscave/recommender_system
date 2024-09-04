from django.shortcuts import render
from suggestions.models import Suggestion
from movies.models import Movie
from django.core.paginator import Paginator
# Create your views here.
def home_view(request):
    context = {}
    user = request.user
    if not user.is_authenticated:
        return render(request, 'home.html', context)

    context['endless_path'] = '/'
    suggestion_qs = Suggestion.objects.filter(user=user, did_rate=False).order_by('-value')
    
    if suggestion_qs.exists():
        movie_ids = suggestion_qs.values_list('object_id', flat=True)
        qs = Movie.objects.by_id_order(movie_ids)
    else:
        qs = Movie.objects.all().order_by('popular')

    # Set up pagination
    paginator = Paginator(qs, 10)  # Show 10 movies per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context['object_list'] = page_obj
    
    if request.htmx:
        return render(request, 'movies/snippet/infinte.html', context)
    
    return render(request, 'dashboard/main.html', context)
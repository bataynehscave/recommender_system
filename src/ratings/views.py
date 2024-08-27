from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.contenttypes.models import ContentType
from .models import Rating
from movies.models import Movie
from django.views.decorators.http import require_http_methods
# Create your views here.

@require_http_methods(['POST'])
def rate_movie_view(request):
    print(request.POST)
    if not request.htmx:
        return HttpResponse("not Allowed", status=400)
    object_id = request.POST.get('object_id')
    rating_value = request.POST.get('rating_value')
    if object_id is None or rating_value is None:
        response =  HttpResponse('nothing here', status=200)
        response['HX-Trigger'] = 'did-skip-movie'
        return response
    user = request.user
    message = "You must login first"
    if user.is_authenticated:
        message= "An Error occured"
        ctype = ContentType.objects.get_for_model(Movie)
        rating_obj = Rating.objects.create(content_type=ctype, object_id=object_id, value=rating_value, user=user)
        if rating_obj.content_object is not None:
            message='rating updated'
            response['HX-Trigger-After-Settle'] = 'did-rate-movie'
            return response
        pass

    return HttpResponse(message, status=200)
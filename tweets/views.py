from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render

from .models import Tweet

# Create your views here.
def home_view(request, *args, **kwargs):
    return HttpResponse("<h1>Hello World</h1>")

def tweet_detail_view(request, tweet_id : int, *args, **kwargs):
    """REST API VIEW
    Consume by JavaScript or Swift
    Args:
        request (_type_): _description_
        tweet_id (int): tweet id

    Raises:
        Http404: Page not found

    Returns:
        _type_: JSON data
    """
    data = {
        "id": tweet_id,
    }
    status = 200
    try:
        obj = Tweet.objects.get(id=tweet_id)
        data['content'] = obj.content
    except:
        data['message'] = "Not found"
        status = 404

    return JsonResponse(data, status=status)
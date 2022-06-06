import random
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render

from .forms import TweetForm
from .models import Tweet

# Create your views here.
def home_view(request, *args, **kwargs):
    # return HttpResponse("<h1>Hello World</h1>")
    return render(request, "pages/home.html", context={}, status=200)

def tweet_create_view(request, *args, **kwargs):
    # TweetForm class can be initialized with data or not
    form = TweetForm(request.POST or None)
    # If the form is valid, we save it directly to DB
    # Otherwise we render it if the form is not valid
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        # Initialize a blank form
        form = TweetForm()
    return render(request, "components/form.html", context={"form": form}, status=200)

def tweet_list_view(request, *args, **kwargs):
    """REST API VIEW

    Args:
        request (_type_): _description_

    Returns:
        _type_: _description_
    """
    qs = Tweet.objects.all()
    tweets_list = [{"id": x.id, "content": x.content, "likes": random.randint(0, 1000)} for x in qs]
    data = {
        "isUser": False,
        "response": tweets_list
    }
    return JsonResponse(data)

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
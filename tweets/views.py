import random
from django.conf import settings
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url

from .forms import TweetForm
from .models import Tweet


ALLOWED_HOSTS = settings.ALLOWED_HOSTS

# Create your views here.
def home_view(request, *args, **kwargs):
    # return HttpResponse("<h1>Hello World</h1>")
    return render(request, "pages/home.html", context={}, status=200)

def tweet_create_view(request, *args, **kwargs):
    # TweetForm class can be initialized with data or not
    form = TweetForm(request.POST or None)
    # Give me the next url
    next_url = request.POST.get("next") or None
    # If the form is valid, we save it directly to DB
    # Otherwise we render it if the form is not valid
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        if request.is_ajax():
            return JsonResponse(obj.serialize(), status=201) # 201 for created items

        if next_url != None and is_safe_url(next_url, ALLOWED_HOSTS):
            return redirect(next_url)
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
    tweets_list = [x.serialize() for x in qs]
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
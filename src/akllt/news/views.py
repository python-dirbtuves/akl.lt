from django.shortcuts import render

from akllt.models import NewsStory


def news_items(request):
    return render(request, 'akllt/news/news_items.html', {
        'news_items': NewsStory.objects.all()[:20]
    })

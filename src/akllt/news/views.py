from django.shortcuts import render, get_object_or_404

from akllt.news.models import NewsStory


def news_items(request):
    return render(request, 'akllt/news/news_items.html', {
        'news_items': NewsStory.objects.all()[:20]
    })


def news_item_details(request, slug):
    news_item = get_object_or_404(NewsStory, slug=slug)
    return render(request, 'akllt/news/news_item_details.html', {
        'news_item': news_item,
    })

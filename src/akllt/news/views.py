from django.shortcuts import render, get_object_or_404

from akllt.news.models import NewsStory


def news_items(request):
    return render(request, 'akllt/news/news_items.html', {
        'news_items': NewsStory.objects.all()[:20]
    })

def news_item(request, slug):
    news_item = get_object_or_404(NewsStory, slug=slug)
    return render(request, 'akllt/news/news_item.html', {
        'news_item': news_item,
    })

def news_details(request, news_item_id):
    news_item = get_object_or_404(NewsStory, pk=news_item_id)
    return render(request, 'akllt/news/news_details.html', {
        'news_item': news_item,
    })

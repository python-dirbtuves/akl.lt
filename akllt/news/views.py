# pylint: disable=too-many-ancestors
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView
from django.utils.text import slugify

from akllt.news.models import NewsStory
from akllt.news.services import get_news_index_page


def news_items(request):
    return render(request, 'akllt/news/news_items.html', {
        'news_items': NewsStory.objects.all()[:20]
    })


def news_item_details(request, slug):
    news_item = get_object_or_404(NewsStory, slug=slug)
    return render(request, 'akllt/news/news_item_details.html', {
        'news_item': news_item,
    })


class NewsStoryCreate(CreateView):
    template_name = 'news/news_form.html'
    model = NewsStory
    fields = ('title', 'body')

    def form_valid(self, form):
        page = form.save(commit=False)
        page.slug = slugify(page.title)

        news_index_page = get_news_index_page()
        news_index_page.add_child(instance=page)

        user = self.request.user if self.request.user.is_authenticated() else None
        page.save_revision(
            user,
            submitted_for_moderation=True,
        )

        return redirect('/')

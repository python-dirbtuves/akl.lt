from django.db import models

from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import MultiFieldPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailimages.models import Image
from wagtail.wagtailsearch import index

from modelcluster.fields import ParentalKey
from modelcluster.tags import ClusterTaggableManager
from taggit.models import TaggedItemBase


class NewsIndex(Page):
    subpage_types = ['news.NewsStory']

    def get_context(self, request, *args, **kwargs):
        return {
            'self': self,
            'request': request,
            'page_title': self.title,
            'news_items': (
                NewsStory.objects.live().descendant_of(self).
                order_by('-date')[:24]
            ),
        }


class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey('news.NewsStory', related_name='news')


class NewsStory(Page):
    date = models.DateField(null=True)
    blurb = RichTextField(blank=True)
    body = RichTextField()
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)
    image = models.ForeignKey(
        Image, null=True, blank=True, on_delete=models.SET_NULL,
        related_name='+'
    )

    search_fields = Page.search_fields + (
        index.SearchField('blurb'),
        index.SearchField('body'),
    )

    def get_context(self, request, *args, **kwargs):
        return {
            'self': self,
            'request': request,
            'page_title': self.title,
        }

NewsStory.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('date'),
    FieldPanel('blurb', classname="full"),
    FieldPanel('body', classname="full"),
]

NewsStory.promote_panels = [
    MultiFieldPanel(Page.promote_panels, "Common page configuration"),
    ImageChooserPanel('image'),
    FieldPanel('tags'),
]

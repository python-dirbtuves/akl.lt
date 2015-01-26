from django.db import models

from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailimages.models import Image
from wagtail.wagtailsearch import index

from modelcluster.fields import ParentalKey


class CategoryPageRelation(models.Model):
    category = ParentalKey('CategoryPage')
    program = ParentalKey('ProgramPage')


class CategoryPage(Page):
    subpage_types = ['programs.ProgramPage']

    def get_context(self, request, *args, **kwargs):
        return {
            'self': self,
            'request': request,
            'page_title': self.title,
            'programs': ProgramPage.objects.live().descendant_of(self)[:24],
        }

CategoryPage.content_panels = [
    FieldPanel('title', classname='full title'),
]


class ProgramPage(Page):
    blurb = RichTextField(blank=True)
    categories = models.ManyToManyField(CategoryPage, through=CategoryPageRelation)
    body = RichTextField()
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

ProgramPage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('categories', classname="full"),
    ImageChooserPanel('image'),
    FieldPanel('blurb', classname="full"),
    FieldPanel('body', classname="full"),
]

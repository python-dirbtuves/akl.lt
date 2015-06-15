from django.forms import ModelForm

from captcha.fields import ReCaptchaField

from akllt.news.models import NewsStory


class NewsStoryForm(ModelForm):

    class Meta:
        model = NewsStory
        fields = ['title', 'body']


class NewsStoryWithCaptchaForm(NewsStoryForm):
    captcha = ReCaptchaField()

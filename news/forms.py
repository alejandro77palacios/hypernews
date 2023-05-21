from django.db import models
from django.forms import ModelForm
from .models import News


class NewsModelForm(ModelForm):
    class Meta:
        model = News
        fields = '__all__'
from django.urls import path

from .views import Coming, SomeNews, MainNews, NewsModelFormView

urlpatterns = [
    path('', Coming.as_view()),
    path('news/', MainNews.as_view()),
    path('news/<int:link>/', SomeNews.as_view()),
    path('news/create/', NewsModelFormView.as_view(), name='create'),
]
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.STATIC_URL)
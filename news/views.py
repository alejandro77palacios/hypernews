import datetime
import json

from django.conf import settings
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic.edit import FormView

from .forms import NewsModelForm

with open(settings.NEWS_JSON_PATH) as f:
    data = json.load(f)


class NewsModelFormView(FormView):
    form_class = NewsModelForm
    template_name = "news/create.html"
    success_url = "/news"

    def form_valid(self, form):
        new_link = max(link['link'] for link in data) + 1
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data.append({'created': date,
                     'text': form.cleaned_data['text'],
                     'title': form.cleaned_data['title'],
                     'link': new_link})
        with open(settings.NEWS_JSON_PATH, 'w') as f:
            json.dump(data, f)
        return redirect('/news')


class MainNews(View):
    def get(self, request, *args, **kwargs):
        all_articles = sorted(data, key=lambda x: x['created'], reverse=True)
        for article in all_articles:
            article["created"] = article["created"][:10]
        query = request.GET.get('q')
        if query:
            filtered_articles = []
            for article in all_articles:
                if query.lower() in article['title'].lower():
                    filtered_articles.append(article)
            all_articles = filtered_articles
            # if not all_articles:
            #     return render(request, 'news/main_news.html')
        context={'data': all_articles}
        return render(request, 'news/main_news.html', context=context)


class SomeNews(View):
    def get(self, request, link, *args, **kwargs):
        with open(settings.NEWS_JSON_PATH) as f:
            data = json.load(f)
        for news in data:
            if news['link'] == link:
                #news['created'] = news['created'][:10]
                return render(request, 'news/some_news.html', context={'news': news})


class Coming(View):
    def get(self, request, *args, **kwargs):
        return redirect('/news/')
        # return render(request, 'news/coming.html')

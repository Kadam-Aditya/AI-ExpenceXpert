from django.shortcuts import render
from newsapi import NewsApiClient


def index(request):
    newsapi = NewsApiClient(api_key='f0d89c00ee804138a24a285d100c64e2')
    top = newsapi.get_top_headlines(category='business')
    my_articles = top['articles']
    news = []
    desc = []
    img = []
    for i in range(len(my_articles)):
        f=my_articles[i]
        news.append(f['title'])
        desc.append(f['description'])
        img.append(f['urlToImage'])
        mylist=zip(news,desc,img)


    return render(request, 'Finance News/index.html', context={'mylist':mylist})
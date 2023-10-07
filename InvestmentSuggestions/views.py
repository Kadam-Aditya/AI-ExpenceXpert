from django.shortcuts import render

def index(request):
    return render(request, 'Investment Suggestions/index.html')

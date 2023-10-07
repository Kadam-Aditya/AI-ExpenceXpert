from django.shortcuts import render

def index(request):
    return render(request, 'Finance News/index.html')
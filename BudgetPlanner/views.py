from django.shortcuts import render

def index(request):
    return render(request, 'Budget Planner/index.html')

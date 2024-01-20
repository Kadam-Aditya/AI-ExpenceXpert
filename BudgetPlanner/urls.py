from django.urls import path
from . import views
from .views import generate_report_view
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [

    path('', views.index, name="Budget Planner"),
    path('generate_report/', generate_report_view, name='generate_report'),
]
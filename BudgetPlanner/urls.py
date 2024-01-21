from django.urls import path
from . import views
from .views import generate_report_view,ai_view,saved_budgets_view,saved_budgets_view1
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [

    path('', views.index, name="Budget Planner"),
    path('Budget Planner/ai_budget', ai_view,name="ai_budget"),
    path('Budget Planner/budget', generate_report_view,name="budget"),
    path('Budget Planner/Saved Budgets', saved_budgets_view, name="Saved Budgets"),
    path('Budget Planner/Saved Budgets1', saved_budgets_view1, name="Saved Budgets1"),
]
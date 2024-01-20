from . import views
from django.urls import path
from .views import update_risk_preference,update_investment_goal

urlpatterns = [
    path('', views.index, name="preferences"),
    path('update_risk_preference/', update_risk_preference, name='update_risk_preference'),
    path('update_investment_goal/', update_investment_goal, name='update_investment_goal'),
]
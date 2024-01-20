from django.shortcuts import render,redirect
import os
import json
from django.conf import settings
from .models import UserPreference
from django.contrib import messages
from django import forms
# Create your views here.


def index(request):
    currency_data = []
    file_path = os.path.join(settings.BASE_DIR, 'currencies.json')

    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        for k, v in data.items():
            currency_data.append({'name': k, 'value': v})

    exists = UserPreference.objects.filter(user=request.user).exists()
    user_preferences = None
    if exists:
        user_preferences = UserPreference.objects.get(user=request.user)
    if request.method == 'GET':

        return render(request, 'preferences/index.html', {'currencies': currency_data,
                                                          'user_preferences': user_preferences})
    else:

        currency = request.POST['currency']
        if exists:
            user_preferences.currency = currency
            user_preferences.save()
        else:
            UserPreference.objects.create(user=request.user, currency=currency)
        messages.success(request, 'Changes saved')
        return render(request, 'preferences/index.html', {'currencies': currency_data, 'user_preferences': user_preferences})



def update_risk_preference(request):
    risk_data = ['High','Moderate','Low']

    exists = UserPreference.objects.filter(user=request.user).exists()
    user_preferences = None
    if exists:
        user_preferences = UserPreference.objects.get(user=request.user)
    if request.method == 'GET':

        return render(request, 'preferences/index.html', {'risk_options': risk_data,
                                                          'user_preferences': user_preferences})
    else:

        risk_preference = request.POST['risk_preference']
        if exists:
            user_preferences.risk_preference = risk_preference
            user_preferences.save()
        else:
            UserPreference.objects.create(user=request.user, risk_preference=risk_preference)
        messages.success(request, 'Changes saved')
        return render(request, 'preferences/index.html', {'risk_options': risk_data, 'user_preferences': user_preferences})


def update_investment_goal(request):
    goal_data = ['Long-term goal','Short-term goal']

    exists = UserPreference.objects.filter(user=request.user).exists()
    user_preferences = None
    if exists:
        user_preferences = UserPreference.objects.get(user=request.user)
    if request.method == 'GET':

        return render(request, 'preferences/index.html', {'goal_options': goal_data,
                                                          'user_preferences': user_preferences})
    else:

        investment_goal = request.POST['investment_goal']
        if exists:
            user_preferences.investment_goal = investment_goal
            user_preferences.save()
        else:
            UserPreference.objects.create(user=request.user, investment_goal=investment_goal)
        messages.success(request, 'Changes saved')
        return render(request, 'preferences/index.html', {'goal_options': goal_data, 'user_preferences': user_preferences})

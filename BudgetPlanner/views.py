from datetime import datetime
import os
from pathlib import Path
import pickle
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from .models import Expense
from .models import ReportDate
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
from joblib import load
from datetime import timedelta
from statsmodels.tsa.arima.model import ARIMA
from sklearn.model_selection import train_test_split
import base64
import joblib
import io
import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX

from matplotlib.backends.backend_agg import FigureCanvasAgg
print(pd.__version__)


def calculate_total_expenses(user, start_date, end_date):
    try:
        # Filter expenses based on the user and date range
        expenses = Expense.objects.filter(owner=user, date__range=[start_date, end_date])

        # Print the SQL query (optional)
        print(expenses.query)

        # Calculate the total sum of expenses
        total_expenses = expenses.aggregate(Sum('amount'))['amount__sum'] or 0

        return total_expenses
    except Exception as e:
        # Handle exceptions as needed (e.g., logging, returning a default value)
        print(f"Error calculating total expenses: {e}")
        return 0
    

def calculate_expenses_by_category(user, start_date, end_date):
    try:
        # Filter expenses based on the user and date range
        expenses = Expense.objects.filter(owner=user, date__range=[start_date, end_date])

        # Calculate total expenses for each category
        expenses_by_category = expenses.values('category').annotate(total_expenses=Sum('amount'))

        # Create a dictionary to store results
        result = {entry['category']: entry['total_expenses'] for entry in expenses_by_category}

        return result
    except Exception as e:
        # Handle exceptions as needed (e.g., logging, returning a default value)
        print(f"Error calculating expenses by category: {e}")
        return {}


# views.py
from .models import ReportDate

def saved_budgets_view1(request):
    if request.method == 'POST':
        budget_id = request.POST.get('budget_id')  # Assuming you have a hidden field in your form for budget_id
        budget = ReportDate.objects.get(id=budget_id)  # Retrieve the budget from the database

        start_date1 = budget.start_date
        end_date1 = budget.end_date
        budget_title = budget.budget_title
        education_budget = budget.education_budget
        medical_budget = budget.medical_budget
        food_budget = budget.food_budget
        entertainment_budget = budget.entertainment_budget
        transport_budget = budget.transport_budget
        personal_care_budget = budget.personal_care_budget
        housing_bills_budget = budget.housing_bills_budget

        total_expenses = calculate_total_expenses(request.user, start_date1, end_date1)
        budget_remaining = budget.total_budget - total_expenses
        expenses_by_category = calculate_expenses_by_category(request.user, start_date1, end_date1)

        return render(request, 'Budget Planner/budget2.html', {
            'total_expenses': total_expenses,
            'start_date': start_date1,
            'end_date': end_date1,
            'budget_remaining': budget_remaining,
            'total_budget': budget.total_budget,
            'expenses_by_category': expenses_by_category,
            'budget_title': budget_title,
            'education_budget': education_budget,
            'medical_budget': medical_budget,
            'food_budget': food_budget,
            'entertainment_budget': entertainment_budget,
            'transport_budget': transport_budget,
            'personal_care_budget': personal_care_budget,
            'housing_bills_budget': housing_bills_budget,
        })
    
    return render(request, 'Budget Planner/budget.html')

def generate_report_view(request):
    if request.method == 'POST':
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')
        budget_str = request.POST.get('total_budget')
        budget_title = request.POST.get('budget_title')
        education_budget = request.POST.get('education_budget')
        medical_budget = request.POST.get('medical_budget')
        food_budget = request.POST.get('food_budget')
        entertainment_budget = request.POST.get('entertainment_budget')
        transport_budget = request.POST.get('transport_budget')
        personal_care_budget = request.POST.get('personal_care_budget')
        housing_bills_budget = request.POST.get('housing_bills_budget')

        start_date1 = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date1 = datetime.strptime(end_date_str, '%Y-%m-%d').date()


        if start_date1 and end_date1:
                
                print(budget_str)
                print(education_budget)
                education_budget = float(education_budget) if education_budget else 0.0
                medical_budget = float(medical_budget) if medical_budget else 0.0
                food_budget = float(food_budget) if food_budget else 0.0
                entertainment_budget = float(entertainment_budget) if entertainment_budget else 0.0
                transport_budget = float(transport_budget) if transport_budget else 0.0
                personal_care_budget = float(personal_care_budget) if personal_care_budget else 0.0
                housing_bills_budget = float(housing_bills_budget) if housing_bills_budget else 0.0


                report = ReportDate(
                    user=request.user,
                    start_date=start_date1,
                    end_date=end_date1,
                    total_budget=float(budget_str),
                    budget_title=budget_title,
                    education_budget=float(education_budget),
                    medical_budget=float(medical_budget),
                    food_budget=float(food_budget),
                    entertainment_budget=float(entertainment_budget),
                    transport_budget=float(transport_budget),
                    personal_care_budget=float(personal_care_budget),
                    housing_bills_budget=float(housing_bills_budget)
                )
                report.save()

      # Pass the user parameter to calculate_total_expenses
                total_expenses = calculate_total_expenses(request.user, start_date1, end_date1)
                budget = float(budget_str)
                budget_remaining = budget-total_expenses
                expenses_by_category = calculate_expenses_by_category(request.user, start_date1, end_date1)

                return render(request, 'Budget Planner/budget2.html', {
                    'total_expenses': total_expenses,
                    'start_date': start_date1,
                    'end_date': end_date1,
                    'budget_remaining': budget_remaining,
                    'total_budget': budget,
                    'expenses_by_category': expenses_by_category,
                    'budget_title': budget_title,
                    'education_budget': education_budget,
                    'medical_budget': medical_budget,
                    'food_budget': food_budget,
                    'entertainment_budget': entertainment_budget,
                    'transport_budget': transport_budget,
                    'personal_care_budget': personal_care_budget,
                    'housing_bills_budget': housing_bills_budget,
 
                })


    return render(request, 'Budget Planner/budget.html')


def index(request):
    return render(request, 'Budget Planner/index.html')

def ai_view(request):
    return render(request, 'Budget Planner/ai_budget.html')


def saved_budgets_view(request):
    saved_budgets = ReportDate.objects.filter(user=request.user)
    return render(request, 'Budget Planner/saved_budgets.html', {'saved_budgets': saved_budgets})


def delete_budget(request, budget_id):
    budget = get_object_or_404(ReportDate, id=budget_id)
    budget.delete()
    saved_budgets = ReportDate.objects.filter(user=request.user)
    return render(request, 'Budget Planner/saved_budgets.html', {'saved_budgets': saved_budgets})


def edit_budget(request, budget_id):
    budget = get_object_or_404(ReportDate, id=budget_id)

    if request.method == 'POST':
        budget.total_budget = request.POST.get('total_budget')
        budget.budget_title = request.POST.get('budget_title')
        budget.education_budget = request.POST.get('education_budget')
        budget.medical_budget = request.POST.get('medical_budget')
        budget.food_budget = request.POST.get('food_budget')
        budget.entertainment_budget = request.POST.get('entertainment_budget')
        budget.transport_budget = request.POST.get('transport_budget')
        budget.personal_care_budget = request.POST.get('personal_care_budget')
        budget.housing_bills_budget = request.POST.get('housing_bills_budget')

        budget.save()
        return redirect('Saved Budgets')  # Redirect to the saved budgets page after editing

    return render(request, 'Budget Planner/edit_budget.html', {'budget': budget})


hyperparameters_dict = {
    'p': 2,
    'd': 1,
    'q': 5,
}

# model = load('D:/ExpenceXpert/ExpenceAI/ARIMA_Model/model.joblib')
models_path = Path('D:/ExpenceXpert/ExpenceAI/ARIMA_Model/models_dict_aggregated.pkl')
params_path = Path('D:/ExpenceXpert/ExpenceAI/ARIMA_Model/best_params_dict_aggregated.pkl')

with open(models_path, 'rb') as models_file:
    models_dict = pickle.load(models_file)

with open(params_path, 'rb') as params_file:
    best_params_dict = pickle.load(params_file)

def generate_budget_plan(user_expenses):
    # model_path = 'D:/ExpenceXpert/ExpenceAI/ARIMA_Model/models_dict_aggregated.pkl'
    # model = joblib.load(model_path)
    user_expenses['date'] = pd.to_datetime(user_expenses['date'])
    
    if 'category' in user_expenses.columns:
        categories = user_expenses['category'].unique()
        print(categories)
        predictions = {}

        try:

            for category in categories:
                print(f"Predicting with ARIMA model for category: {category}")

                category_data = user_expenses[user_expenses['category'] == category]
                ts_data_aggregated_category = category_data.resample('W', on='date')['amount'].sum()
                print(ts_data_aggregated_category)



                # results = models_dict[category].filter(ts_data_aggregated_category.index.min(), ts_data_aggregated_category.index.max())
                results = models_dict[category]
                print('results',results)
                print(results.summary())
                # forecast = results.get_forecast(steps=7) 
                forecast = results.get_prediction(start=ts_data_aggregated_category.index.min(),
                                                  end=ts_data_aggregated_category.index.max() + pd.Timedelta(days=6))
                predicted_values = forecast.predicted_mean.astype(int)
                print('predicted',predicted_values)

                fig, ax = plt.subplots(figsize=(10, 6))
                ax.plot(ts_data_aggregated_category.index, ts_data_aggregated_category, label='User Expenses (Aggregated)')
                ax.plot(predicted_values.index, predicted_values, label='Predicted Values (Aggregated)')
                ax.set_title(f"{category} - ARIMA Model with Time Series Aggregation")
                ax.set_xlabel('Date')
                ax.set_ylabel('Amount')
                ax.legend()

                canvas = FigureCanvasAgg(fig)
                buf = io.BytesIO()
                canvas.print_png(buf)
                buf.seek(0)

                # Convert the image to base64
                encoded_image = base64.b64encode(buf.read()).decode('utf-8')

                predictions[category] = {
                    'user_expenses': ts_data_aggregated_category.tolist(),
                    'predicted_values': predicted_values,
                    'plot_image': encoded_image
                }

        except Exception as e:
            print(f"Error predicting with ARIMA model: {e}")
            return {'error': str(e)}

        finally:
            plt.close()

        return predictions
    else:
        return {'error': 'Category column not found in the DataFrame'}


def budget_planner(request):
    # Assuming you have a form for user input or retrieve expenses from the database
    # In this example, I'm assuming you have a model named Expense
    user_expenses = Expense.objects.all().values('date', 'category', 'amount')

    # Convert user_expenses to a DataFrame
    user_expenses_df = pd.DataFrame(user_expenses)

    # Pass user expenses to the ARIMA model to get predictions
    predictions = generate_budget_plan(user_expenses_df)

    if 'error' in predictions:
        # Handle the case where the 'category' column is not found
        return render(request, 'Budget Planner/ai_budget_result.html', {'error_message': predictions['error']})
    else:
        # Render the template with predictions
        return render(request, 'Budget Planner/ai_budget_result.html', {'predictions': predictions})


def generate_weekly_view(request):
    return render(request, 'Budget Planner/ai_weekly_result.html')

def generate_monthly_view(request):
    return render(request, 'Budget Planner/ai_monthly_result.html')
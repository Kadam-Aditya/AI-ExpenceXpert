from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from .models import Expense
from .models import ReportDate



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



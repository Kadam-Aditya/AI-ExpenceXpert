from datetime import datetime
from django.shortcuts import render
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from .models import Expense



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


def generate_report_view(request):
    if request.method == 'POST':
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')
        budget_str = request.POST.get('budget')

        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

            # Pass the user parameter to calculate_total_expenses
            total_expenses = calculate_total_expenses(request.user, start_date, end_date)
            budget = float(budget_str)
            budget_remaining = budget-total_expenses
            expenses_by_category = calculate_expenses_by_category(request.user, start_date, end_date)

            return render(request, 'Budget Planner/index.html', {
                'total_expenses': total_expenses,
                'start_date': start_date,
                'end_date': end_date,
                'budget_remaining': budget_remaining,
                'total_budget': budget,
                'expenses_by_category': expenses_by_category,
            })
        except ValueError:
            error_message = "Invalid date format. Please use YYYY-MM-DD."
            return render(request, 'Budget Planner/index.html', {'error_message': error_message})

    return render(request, 'Budget Planner/index.html')

def index(request):
    return render(request, 'Budget Planner/index.html')

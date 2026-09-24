from django.shortcuts import render, redirect
from .forms import ExpenseForm
from .models import Expense
from django.db.models import Sum
import datetime

# Create your views here.
def index(request):

    if request.method == "POST":
        expense = ExpenseForm(request.POST)
        if expense.is_valid():
            expense.save()

    # calculate 365 days expense
    last_year = datetime.date.today() - datetime.timedelta(days=365)
    data = Expense.objects.filter(date__gt=last_year)
    yearly_sum = data.aggregate(Sum("amount"))["amount__sum"]

    # calculate 30 days expense
    last_month = datetime.date.today() - datetime.timedelta(days=30)
    data = Expense.objects.filter(date__gt=last_month)
    monthly_sum = data.aggregate(Sum("amount"))["amount__sum"]

    # calculate 7 days expense
    last_week = datetime.date.today() - datetime.timedelta(days=30)
    data = Expense.objects.filter(date__gt=last_week)
    weekly_sum = data.aggregate(Sum("amount"))["amount__sum"]

    # calculate daily sums
    daily_sums = (
        Expense.objects.values("date")
        .order_by("date")
        .annotate(sum=Sum('amount'))
    )

    # category sums
    categorical_sums = (
        Expense.objects.values("category")
        .order_by("date")
        .annotate(sum=Sum('amount'))
    )

    # Get Request
    all_expenses = Expense.objects.all()
    total_expenses = all_expenses.aggregate(Sum("amount"))["amount__sum"]
    expense_from = ExpenseForm()

    return render(request, 'my_app/index.html', {
        "expense_form": expense_from,
        "all_expenses": all_expenses,
        "total_expenses": total_expenses,
        "yearly_sum": yearly_sum,
        "weekly_sum": weekly_sum,
        "monthly_sum": monthly_sum,
        "daily_sums": daily_sums,
        "categorical_sums": categorical_sums,
    })


def edit(request, id):
    expense_detail = Expense.objects.get(id = id)
    expense_form = ExpenseForm(instance = expense_detail)

    if request.method == "POST":
        form = ExpenseForm(request.POST, instance = expense_detail)
        if form.is_valid():
            form.save()
            return redirect("index")

    return render(request, "my_app/edit.html", {
       "expense_form" : expense_form,
    })


def delete(request, id):
    if request.method == "POST":
        expense = Expense.objects.get(id = id)
        expense.delete()
    
    return redirect("index")
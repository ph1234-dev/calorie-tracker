
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Food, User

import calendar
from datetime import date


import calendar
from datetime import date, datetime
from django.db.models import Sum
from django.db.models.functions import TruncDate


from .forms import RegisterForm , LoginForm, FoodForm
# views.py

def index(request):
    if request.user.is_authenticated:
        return redirect("tracker:dashboard")  # change to your actual dashboard URL name

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            login(request, form.user)
            return redirect("tracker:dashboard")
    else:
        form = LoginForm()

    # return render(request, "tracker/index.html",form)
    return render(request, "tracker/index.html", {"form": form})


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Basic fields
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data.get('email', '')

            # Extra fields
            first_name = form.cleaned_data.get('first_name', '')
            middle_name = form.cleaned_data.get('middle_name', '')
            last_name = form.cleaned_data.get('last_name', '')
            date_of_birth = form.cleaned_data.get('date_of_birth', None)
            address = form.cleaned_data.get('address', '')
            occupation = form.cleaned_data.get('occupation', '')

            # Create user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                middle_name=middle_name,
                date_of_birth=date_of_birth,
                address=address,
                occupation=occupation,
            )

            # Log the user in
            login(request, user)
            return redirect("tracker:index")
    else:
        form = RegisterForm()

    return render(request, "tracker/pages/register.html", {"form": form})



def user_logout(request):
    logout(request)
    return redirect("tracker:index")


@login_required
def add_food(request):

    # select date today
    today = date.today()
    year = today.year
    month = today.month
    day = today.day

    # timezone-aware datetime (use noon to avoid edge cases)
    selected_date = timezone.make_aware(
        datetime(year, month, day, 12, 0)
    )
    if request.method == "POST":
        form = FoodForm(request.POST)
        if form.is_valid():
            Food.objects.create(
                user=request.user,
                description=form.cleaned_data["description"],
                serving_size=form.cleaned_data.get("serving_size", ""),
                estimated_calories=form.cleaned_data["calories"],
                details=form.cleaned_data.get("details", ""),
                created_at=selected_date,  # saved for selected date
            )
            return redirect(f"{request.path}?year={year}&month={month}&day={day}")
    else:
        form = FoodForm()

    # Filter foods for this user AND selected date
    foods_for_date = request.user.foods.filter(created_at__date=selected_date.date())
    
    return render(request, "tracker/pages/add_food_today.html", {
        "selected_date": selected_date,
        "foods": foods_for_date,
        "year": year,
        "month": month,
        "day": day,
        "form": form,
    })



@login_required
def dashboard(request):
    
    today = date.today()

    # Get year/month from query params; fallback to current month
    year = int(request.GET.get("year", today.year))
    month = int(request.GET.get("month", today.month))

    # Create calendar for the month
    cal = calendar.Calendar(calendar.SUNDAY)
    month_days = cal.monthdayscalendar(year, month)

        # Get calories taken today by user
    today_calories = (
        Food.objects
        .filter(user=request.user, created_at__date=today)
        .aggregate(total=Sum("estimated_calories"))
        .get("total") or 0
    )

    # Get user-specific calories per day
    calories_qs = (
        Food.objects
        .filter(user=request.user, created_at__year=year, created_at__month=month)
        .annotate(day=TruncDate("created_at"))
        .values("day")
        .annotate(total_calories=Sum("estimated_calories"))
    )

    calories_per_day = {item["day"].day: item["total_calories"] for item in calories_qs}

    # Build calendar data for template
    calendar_data = []
    for week in month_days:
        week_data = []
        for day in week:
            if day == 0:
                week_data.append(None)
            else:
                week_data.append({
                    "day": day,
                    "calories": calories_per_day.get(day, 0),
                    "is_today": today.year == year and today.month == month and today.day == day
                })
        calendar_data.append(week_data)

    # Previous and next month logic
    prev_month = month - 1 if month > 1 else 12
    prev_year = year if month > 1 else year - 1

    next_month = month + 1 if month < 12 else 1
    next_year = year if month < 12 else year + 1

    context = {
        "year": year,
        "month": month,
        "month_name": calendar.month_name[month],
        "calendar_data": calendar_data,
        "prev_year": prev_year,
        "prev_month": prev_month,
        "next_year": next_year,
        "next_month": next_month,
        "today_calories": today_calories,  
    }

    return render(request, "tracker/pages/dashboard.html", context)



@login_required
def dashboard_add_food(request):
    # Date selected from calendar (default today)
    year = int(request.GET.get("year", date.today().year))
    month = int(request.GET.get("month", date.today().month))
    day = int(request.GET.get("day", date.today().day))

    # Make the selected date timezone-aware (set noon to avoid timezone issues)
    selected_date = timezone.make_aware(datetime(year, month, day))

    if request.method == "POST":
        form = FoodForm(request.POST)
        if form.is_valid():
            Food.objects.create(
                user=request.user,
                description=form.cleaned_data["description"],
                serving_size=form.cleaned_data.get("serving_size", ""),
                estimated_calories=form.cleaned_data["calories"],
                details=form.cleaned_data.get("details", ""),
                created_at=selected_date,  # saved for selected date
            )
            return redirect(f"{request.path}?year={year}&month={month}&day={day}")
    else:
        form = FoodForm()

    # Filter foods for this user AND selected date
    foods_for_date = request.user.foods.filter(created_at__date=selected_date.date())

    
    
    return render(request, "tracker/pages/dashboard_add_food.html", {
        "selected_date": selected_date,
        "foods": foods_for_date,
        "year": year,
        "month": month,
        "day": day,
        "form": form,
    })

@login_required
def dashboard_delete_food(request, food_id):
    food = get_object_or_404(Food, id=food_id, user=request.user)

    if request.method == "POST":
        food.delete()

    return redirect("tracker:dashboard_add_food")


@login_required
def dashboard_update_food(request, food_id):
    # Get the food for this user
    food = get_object_or_404(Food, id=food_id, user=request.user)

    # Get year/month/day from query params; fallback to today
    year = int(request.GET.get("year", date.today().year))
    month = int(request.GET.get("month", date.today().month))
    day = int(request.GET.get("day", date.today().day))

    if request.method == "POST":
        # Get the new calories value from the form
        new_calories = request.POST.get("update")
        if new_calories:
            food.estimated_calories = int(new_calories)
            food.save()

    # Redirect back to dashboard_add_food with the same date
    return redirect(f"{reverse('tracker:dashboard_add_food')}?year={year}&month={month}&day={day}")

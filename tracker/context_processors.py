from datetime import date
from django.db.models import Sum
from .models import Food

def context_processor_calculate_today_calories(request):
    """
    Adds today's total calories and today's date for the logged-in user to the template context.
    """
    if request.user.is_authenticated:
        today = date.today()
        total = (
            Food.objects
            .filter(user=request.user, created_at__date=today)
            .aggregate(total=Sum("estimated_calories"))
            .get("total") or 0
        )
    else:
        today = date.today()
        total = 0

    # Return a dictionary with valid key-value pairs
    return {
        "context_processor_calculate_today_calories": total,
        "context_processor_calculate_today_calories_today_date": today
    }
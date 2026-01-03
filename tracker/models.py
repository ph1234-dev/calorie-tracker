from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date

from django.conf import settings  # needed for ForeignKey to custom user


# first_name, last_name, username, email, password already exist in AbstractUser
class User(AbstractUser):
    middle_name = models.CharField(max_length=150, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    occupation = models.CharField(max_length=150, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

    @property
    def age(self):
        if not self.date_of_birth:
            return None
        today = date.today()
        return (
            today.year
            - self.date_of_birth.year
            - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        )


    
class Food(models.Model):
    user = models.ForeignKey( 
        settings.AUTH_USER_MODEL,  # ✅ always use this with custom user
        on_delete=models.CASCADE,
        related_name="foods",
        null=True,       # allow existing rows to have NULL
        blank=True
    )
    description = models.CharField(max_length=100)
    details = models.TextField(blank=True)
    serving_size = models.CharField(max_length=50)
    estimated_calories = models.IntegerField()
    
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.description} ({self.serving_size}) - {self.estimated_calories} kcal"
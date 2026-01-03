from django.urls import path
from . import views

# this is the namespace .. mandatory so that you can call href="{% url 'sdg:index' %}"
app_name = 'tracker' 

urlpatterns = [
    path("",views.index, name="index"),
    # no leading / in all of the routes
    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('add-food/', views.add_food, name='add_food'),
    path("dashboard/",views.dashboard, name="dashboard"),
    path("dashboard/add",views.dashboard_add_food, name="dashboard_add_food"),
    path("dashboard/<int:food_id>/delete/", views.dashboard_delete_food, name="delete_food"),
    path("dashboard/<int:food_id>/update/", views.dashboard_update_food, name="update_food"),
]
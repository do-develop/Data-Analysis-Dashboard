from django.urls import path
from . import views

urlpatterns = [
    path('countries/', views.country_list, name='country_list'),
    path('', views.dashboard_with_pivot, name='dashboard_with_pivot'),
    path('data', views.pivot_data, name='pivot_data'),
]

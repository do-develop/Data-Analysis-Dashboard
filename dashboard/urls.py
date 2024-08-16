from django.urls import path
from . import views

urlpatterns = [
    path('countries/', views.country_list, name='country_list'),
    path('details/<str:country_code>/', views.country_detail, name='country_detail'),
    path('', views.international_debt_statistics_data, name='dataset'),
]

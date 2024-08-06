from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import render
from django.core import serializers
from .models import Country, Series, Data


def country_list(request):
    countries = Country.objects.all()
    return render(request, 'dashboard/country_list.html', {'countries': countries})

def dashboard_with_pivot(request):
    return render(request, 'dashboard.html', {})

def pivot_data(request):
    dataset = Data.objects.all()
    data = serializers.serialize('json', dataset)
    return JsonResponse(data, safe=False)
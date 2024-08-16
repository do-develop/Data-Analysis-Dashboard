from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import render
from django.core import serializers
from django.db.models import Max, Sum, Count
from .models import Country, Series, Data
from datetime import datetime
import logging


# Get an instance of a logger
logger = logging.getLogger('mylogeer')

def country_list(request):
    countries = Country.objects.all()
    for data in countries:
        print('country code', data)
    return render(request, 'dashboard/country_list.html', {'countries': countries})

def international_debt_statistics_data(request):
    dataset = Data.objects.all()
    data_year = 2018
    total_countries = dataset.values('country_code').distinct().count()
    year_data = dataset.filter(year=data_year).values('country_code').annotate(total_amount=Sum('amount'))
    # print(f"Current Year Data: {year_data}")
    countries = [entry['country_code'] for entry in year_data]
    amounts = [float(entry['total_amount']) for entry in year_data] 
    

    distribution_data = Country.objects.values('region', 'income_group').annotate(count=Count('code')).order_by('region')

    # region, income_group, count
    distributions = {}
    for item in distribution_data:
        region = item['region']
        income_group = item['income_group']
        count = item['count']
        
        # Initialize the region key if not present
        if region not in distributions:
            distributions[region] = {}
        
        # Add income group count
        distributions[region][income_group] = count

    regions_data = []
    for region, income_groups in distributions.items():
        labels = list(income_groups.keys())
        data = list(income_groups.values())
        if region:
            regions_data.append({
                'region': region,
                'labels': labels,
                'data': data
            })
    
    context = {
        'total_countries': total_countries,
        'data_year': data_year,
        'countries': countries,
        'amounts': amounts,

        'regions_data': regions_data,
    }

    return render(request, 'dashboard.html', context)


def income_group_distribution_by_region(request):
    
    return render(request, 'dashboard.html', context)

# def pivot_data(request):
#     # dataset = Data.objects.all()
#     # data = serializers.serialize('json', dataset)
#     return JsonResponse(data, safe=False)

def country_detail(request, country_code):
    detailed_data = Data.objects.filter(country_code=country_code, year__range=(2018,2020))
    country_data = Country.objects.filter(code=country_code)

    # Initialize a dictionary to hold data grouped by year
    grouped_data = {}

    for detail in detailed_data:
        year = detail.year
        series_code = detail.series_code.code
        amount = float(detail.amount)
        
        # Ensure the year key exists in the grouped_data dictionary
        if year not in grouped_data:
            grouped_data[year] = {'labels': [], 'amounts': []}
        
        # Add the series_code and amount to the corresponding year
        grouped_data[year]['labels'].append(series_code)
        grouped_data[year]['amounts'].append(amount)

    context = {
        'country_code': country_code,
        'country_name': country_data[0].long_name,
        'grouped_data': grouped_data,
    }

    return render(request, 'detail.html', context)


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
    debt_series_code = 'DT.DOD.DECT.CD' # External Debt (Total, current US$)
    year_data = dataset.filter(year=data_year, series_code=debt_series_code)
    
    valid_countries = Country.objects.exclude(region=None).values_list('code', flat='True')
    year_data = year_data.filter(country_code__in=valid_countries)
    total_countries = year_data.values('country_code').distinct().count()
    country_debt_data = year_data.values('country_code').annotate(total_amount=Sum('amount')).order_by('country_code')

    countries = [entry['country_code'] for entry in country_debt_data]
    print("countries data: ", countries)
    amounts = [float(entry['total_amount']) for entry in country_debt_data]
    

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



# https://www.kaggle.com/code/salmaneunus/international-debt-statistics-analysis/notebook
# Which country owns the maximum amount of debt and what does that amount look like?


# What is the average amount of debt owed by countries across different debt indicators?

'''
# IDEA 1 - Show how the distribution of countries across different income groups has changed over the years.
# In stacked area chart, group countries by income_group and year, then count the number of countries in each income group for each year.

# IDEA 2 - Analyze the trend of various economic indicators over time for a specific country or region.
# Line Chart with Multiple Series (Filter the Data model by country_code and series_code, and plot the amount over the year. You can allow users to select different series codes to visualize trends of different indicators.)

# IDEA 3 - Compare specific economic indicators (like GDP per capita, external debt, etc.) across different regions.
# Bar Chart with Grouped Data - For a selected year, group data by region and series_code, then plot the amount for each region.
'''
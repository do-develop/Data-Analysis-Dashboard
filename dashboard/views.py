from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import render
from django.core import serializers
from django.db.models import Max, Sum, Count, Avg
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
    # PART 1 - Total Debt by Countries
    data_year = 2018    
    debt_series_code = 'DT.DOD.DECT.CD' # External Debt (Total, current US$)
    year_data = dataset.filter(year=data_year, series_code=debt_series_code)
    
    valid_countries = Country.objects.exclude(region=None).values_list('code', flat='True')
    year_data = year_data.filter(country_code__in=valid_countries)
    total_countries = year_data.values('country_code').distinct().count()
    country_debt_data = year_data.values('country_code').annotate(total_amount=Sum('amount')).order_by('country_code')

    countries = [entry['country_code'] for entry in country_debt_data]
    amounts = [float(entry['total_amount']) for entry in country_debt_data]
    

    # PART 2 - Income Distribution by Region
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



def country_detail(request, country_code):
    country_data = Country.objects.filter(code=country_code)
    detailed_data = Data.objects.filter(
        country_code=country_code, year__range=(2018,2020)
        ).select_related('series_code')
    # Top 5 average amount of debt for each series code
    average_debt = detailed_data.values('series_code').annotate(
        average_amount=Avg('amount')
    ).order_by('-average_amount')[:5]

    series_codes = [item['series_code'] for item in average_debt]
    series_details = Series.objects.filter(code__in=series_codes).values('code', 'indicator_name', 'long_definition')
    series_map = {item['code']: {
            'indicator_name': item['indicator_name'],
            'long_definition': item['long_definition']
        } for item in series_details}

    # Prepare data for Chart.js
    chart_data = {
        'labels': [],
        'data': [],
        'series_details': []
    }

    for item in average_debt:
        series_code = item['series_code']
        average_amt = float(item['average_amount'])
        details = series_map.get(series_code, {})

        chart_data['labels'].append(details.get('indicator_name', 'Unknown'))
        chart_data['data'].append(average_amt)
        chart_data['series_details'].append({
            'code': series_code,
            'indicator_name': details.get('indicator_name', 'Unknown'),
            'long_definition': details.get('long_definition', 'N/A')
        })
    
    context = {
        'country_code': country_code,
        'country_name': country_data[0].long_name,
        'chart_data': chart_data
    }

    print('context: ', context)
    return render(request, 'detail.html', context)



'''
# IDEA 1 - Show how the distribution of countries across different income groups has changed over the years.
# In stacked area chart, group countries by income_group and year, then count the number of countries in each income group for each year.

# IDEA 2 - Analyze the trend of various economic indicators over time for a specific country or region.
# Line Chart with Multiple Series (Filter the Data model by country_code and series_code, and plot the amount over the year. You can allow users to select different series codes to visualize trends of different indicators.)

# IDEA 3 - Compare specific economic indicators (like GDP per capita, external debt, etc.) across different regions.
# Bar Chart with Grouped Data - For a selected year, group data by region and series_code, then plot the amount for each region.
'''
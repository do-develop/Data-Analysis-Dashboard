# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Country(models.Model):
    code = models.CharField(primary_key=True, max_length=3)
    long_name = models.CharField(max_length=255, blank=True, null=True)
    income_group = models.CharField(max_length=50, blank=True, null=True)
    region = models.CharField(max_length=100, blank=True, null=True)
    lending_category = models.CharField(max_length=10, blank=True, null=True)
    other_groups = models.CharField(max_length=50, blank=True, null=True)
    currency_unit = models.CharField(max_length=50, blank=True, null=True)
    latest_household_survey = models.CharField(max_length=255, blank=True, null=True)
    national_accounts_base_year = models.CharField(max_length=50, blank=True, null=True)
    national_accounts_reference_year = models.CharField(max_length=50, blank=True, null=True)
    system_of_trade = models.CharField(max_length=50, blank=True, null=True)
    government_accounting_concept = models.CharField(max_length=50, blank=True, null=True)
    imf_data_dissemination_standard = models.CharField(max_length=100, blank=True, null=True)
    source_of_most_recent_income_and_expenditure_data = models.CharField(max_length=255, blank=True, null=True)
    vital_registration_complete = models.BooleanField(blank=True, null=True)
    alpha_2_code = models.CharField(max_length=2, blank=True, null=True)
    wb_2_code = models.CharField(max_length=2, blank=True, null=True)
    short_name = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'country'


class Data(models.Model):
    country_code = models.ForeignKey('Country', models.DO_NOTHING, db_column='country_code', primary_key=True)
    series_code = models.ForeignKey('Series', models.DO_NOTHING, db_column='series_code')
    year = models.DecimalField(max_digits=65535, decimal_places=65535)
    amount = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'data'
        unique_together = (('country_code', 'series_code', 'year'),)

class Series(models.Model):
    code = models.CharField(primary_key=True, max_length=32)
    indicator_name = models.CharField(max_length=255, blank=True, null=True)
    short_definition = models.TextField(blank=True, null=True)
    long_definition = models.TextField(blank=True, null=True)
    aggregation_method = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'series'

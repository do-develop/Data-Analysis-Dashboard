# Generated by Django 5.0.7 on 2024-08-06 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('code', models.CharField(max_length=3, primary_key=True, serialize=False)),
                ('long_name', models.CharField(blank=True, max_length=255, null=True)),
                ('income_group', models.CharField(blank=True, max_length=50, null=True)),
                ('region', models.CharField(blank=True, max_length=100, null=True)),
                ('lending_category', models.CharField(blank=True, max_length=10, null=True)),
                ('other_groups', models.CharField(blank=True, max_length=50, null=True)),
                ('currency_unit', models.CharField(blank=True, max_length=50, null=True)),
                ('latest_household_survey', models.CharField(blank=True, max_length=255, null=True)),
                ('national_accounts_base_year', models.CharField(blank=True, max_length=50, null=True)),
                ('national_accounts_reference_year', models.CharField(blank=True, max_length=50, null=True)),
                ('system_of_trade', models.CharField(blank=True, max_length=50, null=True)),
                ('government_accounting_concept', models.CharField(blank=True, max_length=50, null=True)),
                ('imf_data_dissemination_standard', models.CharField(blank=True, max_length=100, null=True)),
                ('source_of_most_recent_income_and_expenditure_data', models.CharField(blank=True, max_length=255, null=True)),
                ('vital_registration_complete', models.BooleanField(blank=True, null=True)),
                ('alpha_2_code', models.CharField(blank=True, max_length=2, null=True)),
                ('wb_2_code', models.CharField(blank=True, max_length=2, null=True)),
                ('short_name', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'db_table': 'country',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.DecimalField(blank=True, decimal_places=65535, max_digits=65535, null=True)),
                ('amount', models.DecimalField(blank=True, decimal_places=65535, max_digits=65535, null=True)),
            ],
            options={
                'db_table': 'data',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Series',
            fields=[
                ('code', models.CharField(max_length=32, primary_key=True, serialize=False)),
                ('indicator_name', models.CharField(blank=True, max_length=255, null=True)),
                ('short_definition', models.TextField(blank=True, null=True)),
                ('long_definition', models.TextField(blank=True, null=True)),
                ('aggregation_method', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'db_table': 'series',
                'managed': False,
            },
        ),
    ]

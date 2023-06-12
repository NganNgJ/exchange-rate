# Generated by Django 3.1 on 2023-06-10 06:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=255)),
                ('symbol', models.CharField(default='', max_length=255)),
                ('status', models.CharField(default='ACTIVE', max_length=255)),
            ],
            options={
                'db_table': 'currencies',
            },
        ),
        migrations.CreateModel(
            name='Exchangerate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.FloatField(default=1)),
                ('end_currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='end_currency', to='api.currency')),
                ('start_currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='start_currency', to='api.currency')),
            ],
            options={
                'db_table': 'exchange_currency_rates',
            },
        ),
        migrations.CreateModel(
            name='ExchangerateHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.FloatField(default=1)),
                ('from_date', models.DateTimeField(null=True)),
                ('end_date', models.DateTimeField(null=True)),
                ('exchange_rate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.exchangerate')),
            ],
            options={
                'db_table': 'exchange_currency_rate_histories',
            },
        ),
    ]
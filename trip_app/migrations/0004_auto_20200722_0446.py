# Generated by Django 2.2 on 2020-07-22 11:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trip_app', '0003_auto_20200721_2145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='trip',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trip_expenses', to='trip_app.Trip'),
        ),
    ]
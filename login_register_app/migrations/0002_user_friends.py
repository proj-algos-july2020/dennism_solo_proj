# Generated by Django 2.2 on 2020-07-20 04:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login_register_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='friends',
            field=models.ManyToManyField(related_name='_user_friends_+', to='login_register_app.User'),
        ),
    ]
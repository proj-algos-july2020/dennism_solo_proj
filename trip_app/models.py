from __future__ import unicode_literals
from django.db import models
from datetime import datetime
from login_register_app.models import User

class TripManager(models.Manager):
    def trip_validator(self,postData):
        errors = {}
        if postData['city'] == '':
            errors['city'] = 'City is required.'

        if postData['country'] == '':
            errors['country'] = 'Country is required.'

        if postData['state'] != '':
            if len(postData['state']) != 2:
                errors['state'] = 'State must have 2 characters.'

        if postData['start_date'] == '':
            errors['start_date'] = "Trip start date is required."
        
        if postData['end_date'] == '':
            errors['end_date'] = "Trip end date is required!"

        if postData['start_date'] != '' and postData['end_date'] != '':
            start = datetime.strptime(postData['start_date'], "%Y-%m-%d")
            end = datetime.strptime(postData['end_date'], "%Y-%m-%d")
            if start > end:
                errors['start_date'] = "Time travel is not allowed!"
        return errors
    
    def expense_validator(self,postData):
        errors = {}
        if postData['amount'] == '':
            errors['amount'] = 'Amount of expense is required.'
        return errors

    def itinerary_validator(self,postData):
        errors = {}
        if postData['date'] == '':
            errors['date'] = 'Activity date is required.'

        if postData['start_time'] == '':
            errors['start_time'] = 'Start time is required.'

        if postData['end_time'] == '':
            errors['end_time'] = 'End time is required.'

        if postData['start_time'] != '' and postData['end_time'] != '':
            start = postData['start_time']
            end = postData['end_time']
            if start > end:
                errors['start_time'] = 'Time travel is not allowed!'
        
        if postData['activity'] == '':
            errors['activity'] = 'Activity description is required.'
        return errors

class Trip(models.Model):
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    state = models.CharField(max_length=255,blank=True)
    place = models.CharField(max_length=255,blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    created_by = models.ForeignKey(User, related_name="trips_created", on_delete=models.CASCADE)
    users_joined = models.ManyToManyField(User, related_name="trips_joined")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TripManager()
    
class Expense(models.Model):
    amount = models.DecimalField(decimal_places=2, max_digits=100)
    paid_by = models.ForeignKey(User, related_name="expenses_paid", on_delete=models.CASCADE)
    notes = models.TextField()
    trip = models.ForeignKey(Trip, related_name="trip_expenses", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TripManager()

class Itinerary(models.Model):
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    activity = models.CharField(max_length=255)
    address = models.CharField(max_length=255, blank=True)
    notes = models.TextField()
    trip = models.ForeignKey(Trip, related_name="trip_activities", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TripManager()

class PhotoAlbum(models.Model):
    photo = models.ImageField()
    trip = models.ForeignKey(Trip, related_name="trip_photos", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

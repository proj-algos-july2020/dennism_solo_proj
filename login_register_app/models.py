from __future__ import unicode_literals
from django.db import models
from datetime import datetime
import re
import bcrypt

# User Login and Registrarion validator
class UserManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        if postData['first_name'] != '':
            if not postData['first_name'].isalpha():
                errors['first_name'] = "Invalid characters. First name should be alphabetic only."
            elif len(postData['first_name']) < 2:
                errors['first_name'] = "First name should be at least 2 characters."
        else:
            errors['first_name'] = "First name is required."
        
        if postData['last_name'] != '':
            if not postData['first_name'].isalpha():
                errors['first_name'] = "Invalid characters. Last name should be alphabetic only."
            elif len(postData['last_name']) < 2:
                errors['last_name'] = "Last name should be at least 2 characters."   
        else:
            errors['last_name'] = "Last name is required."  
        
        if postData['birthday'] != '':
            bday = postData['birthday']
            bday = datetime.strptime(bday, "%Y-%m-%d")
            today = datetime.today()
            if bday > today:
                errors['birthday'] = "Date of Birth should be in the past."
            elif today.year - bday.year - ((today.month, today.day) < (bday.month, bday.year)) < 13:
                errors['birthday'] = "Age should be at least 13 years old."
        else:
            errors['birthday'] = "Date of Birth is required."
        
        if postData['email'] != '':
            curr_email = postData['email'].lower()
            if not EMAIL_REGEX.match(curr_email):
                errors['email'] = "Invalid email address."
            elif User.objects.filter(email__iexact=curr_email).exists():
                errors['email'] = "Email already exists in the database."
        else:
            errors['email'] = "Email is required."
        
        if postData['password'] != '':
            if len(postData['password']) < 8:
                errors['password'] = "Password should be at least 8 characters."
            elif not postData['password'] == postData['pw_confirm']:
                errors['password'] = "Password does not match."
        else:
            errors['password'] = "Password is required."
        return errors
    
    def login_validator(self, postData):
        errors = {}
        curr_email = postData['email_login'].lower()
        if not User.objects.filter(email__iexact=curr_email).exists():
            errors['email_login'] = "Sorry. We don't recognize this email"
        else:
            curr_user = User.objects.get(email=curr_email)
            if not bcrypt.checkpw(postData['pw_login'].encode(), curr_user.password.encode()):
                errors['pw_login'] = "Invalid password. Please try again"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    birthday = models.DateField()
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

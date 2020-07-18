from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
import bcrypt

# function for user registration
def register(request):
    errors = User.objects.register_validator(request.POST)
    request.session['action'] = "registered"
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        new_user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'].lower(), birthday=request.POST['birthday'], password=pw_hash)
        request.session['user_id'] = new_user.id
        return redirect('/')

def index(request):
    return render(request, 'login_page.html')

def login(request):
    errors = User.objects.login_validator(request.POST)
    request.session['action'] = "logged in"
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        logged_email = request.POST['email_login'].lower()
        user = User.objects.filter(email=logged_email)
        if user:
            logged_user = user[0]
            if bcrypt.checkpw(request.POST['pw_login'].encode(), logged_user.password.encode()):
                request.session['user_id'] = logged_user.id
                return redirect('/success')
        return redirect('/')

def logout(request):
    request.session.flush()
    return redirect('/')

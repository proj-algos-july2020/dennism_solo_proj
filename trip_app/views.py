from django.shortcuts import render, redirect
from django.contrib import messages
from login_register_app.models import User
from .models import Trip, Expense, Itinerary, PhotoAlbum

def user_dashboard(request):
    context = {
        "all_trips": Trip.objects.all(),
        "curr_user": User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'user_dashboard.html', context)

def trip_dashboard(request):
    context = {
        "all_trips": Trip.objects.all(),
        "curr_user": User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'trip_dashboard.html', context)

def friends_dashboard(request):
    context = {
        "curr_user": User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'friends_dashboard.html', context)

def itinerary_dashboard(request, trip_id):
    context = {
        "curr_trip": Trip.objects.get(id=trip_id)
    }
    return render(request, 'itinerary.html', context)

def expense_log(request, trip_id):
    context = {
        "curr_trip": Trip.objects.get(id=trip_id)
    }
    return render(request, 'expense_log.html', context)

def edit_dashboard(request, trip_id):
    context = {
        "curr_trip": Trip.objects.get(id=trip_id)
    }
    return render(request, 'edit_trip.html', context)

def view_dashboard(request, trip_id):
    context = {
        "curr_trip": Trip.objects.get(id=trip_id)
    }
    return render(request, 'view_trip.html', context)

def add_dashboard(request):
    context = {
        "curr_user": User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'add_trip.html', context)

def add_trip(request):
    if 'cancel_trip' in request.POST:
        return redirect('/dashboard/trips')
    errors = Trip.objects.trip_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/dashboard/trips/new')
    else:
        curr_user = User.objects.get(id=request.session['user_id'])
        new_trip = Trip.objects.create(city=request.POST['city'], country=request.POST['country'], state=request.POST['state'], place=request.POST['place'], start_date=request.POST['start_date'], end_date=request.POST['end_date'], created_by=curr_user)
        new_trip.users_joined.add(curr_user)
        return redirect('/dashboard/trips')

def edit_trip(request, trip_id):
    if 'cancel_trip' in request.POST:
        return redirect('/dashboard/trips')
    errors = Trip.objects.trip_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/dashboard/trips/edit/{trip_id}')
    else:
        curr_trip = Trip.objects.get(id=trip_id)
        curr_trip.city = request.POST['city']
        curr_trip.country = request.POST['country']
        curr_trip.state = request.POST['state']
        curr_trip.place = request.POST['place']
        curr_trip.start_date = request.POST['start_date']
        curr_trip.end_date = request.POST['end_date']
        curr_trip.save()
        return redirect('/dashboard/trips')
    
def remove_trip(request, trip_id):
    curr_trip = Trip.objects.get(id=trip_id)
    curr_trip.delete()
    return redirect('/dashboard/trips')

def add_remove_participant(request, trip_id):
    user_added = User.objects.get(id=request.POST['participant'])
    curr_trip = Trip.objects.get(id=trip_id)
    if user_added in curr_trip.users_joined.all():
        curr_trip.users_joined.remove(user_added)
    else:
        curr_trip.users_joined.add(user_added)
    return redirect(f'/dashboard/trips/view/{trip_id}')

def add_friend(request):
    
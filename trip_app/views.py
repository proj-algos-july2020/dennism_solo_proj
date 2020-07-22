from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime
from login_register_app.models import User
from .models import Trip, Expense, Itinerary, PhotoAlbum

def user_dashboard(request):
    context = {
        "all_trips": Trip.objects.all(),
        "curr_user": User.objects.get(id=request.session['user_id']),
        "today": datetime.now()
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
        "curr_user": User.objects.get(id=request.session['user_id']),
        "all_users": User.objects.all()
    }
    return render(request, 'friends_dashboard.html', context)

def itinerary_dashboard(request, trip_id):
    context = {
        "curr_user": User.objects.get(id=request.session['user_id']),
        "curr_trip": Trip.objects.get(id=trip_id)
    }
    return render(request, 'itinerary.html', context)

def edit_activity_dashboard(request, trip_id, itinerary_id):
    context = {
        "curr_user": User.objects.get(id=request.session['user_id']),
        "curr_trip": Trip.objects.get(id=trip_id),
        "curr_activity": Itinerary.objects.get(id=itinerary_id)
    }
    return render(request, 'edit_itinerary.html', context)

def expense_log(request, trip_id):
    context = {
        "curr_user": User.objects.get(id=request.session['user_id']),
        "curr_trip": Trip.objects.get(id=trip_id)
    }
    return render(request, 'expense_log.html', context)

def edit_expense_dashboard(request, trip_id, expense_id):
    context = {
        "curr_user": User.objects.get(id=request.session['user_id']),
        "curr_trip": Trip.objects.get(id=trip_id),
        "curr_expense": Expense.objects.get(id=expense_id)
    }
    return render(request, 'edit_expense.html', context)

def edit_dashboard(request, trip_id):
    context = {
        "curr_trip": Trip.objects.get(id=trip_id),
        "curr_user": User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'edit_trip.html', context)

def view_dashboard(request, trip_id):
    if 'delete_trip' in  request.GET:
        return redirect(f'/dashboard/trips/{trip_id}/remove')
    context = {
        "curr_user": User.objects.get(id=request.session['user_id']),
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
        new_trip = Trip.objects.create(city=request.POST['city'], country=request.POST['country'], state=request.POST['state'].upper(), place=request.POST['place'], start_date=request.POST['start_date'], end_date=request.POST['end_date'], created_by=curr_user)
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
        curr_trip.state = request.POST['state'].upper()
        curr_trip.place = request.POST['place']
        curr_trip.start_date = request.POST['start_date']
        curr_trip.end_date = request.POST['end_date']
        curr_trip.save()
        return redirect('/dashboard/trips')
    
def remove_trip(request, trip_id):
    curr_trip = Trip.objects.get(id=trip_id)
    curr_trip.delete()
    return redirect('/dashboard/trips')

def leave_trip(request, trip_id):
    curr_user = User.objects.get(id=request.session['user_id'])
    curr_trip = Trip.objects.get(id=trip_id)
    curr_trip.users_joined.remove(curr_user)
    return redirect('/dashboard/trips')

def add_remove_participant(request, trip_id):
    user_added = User.objects.get(id=request.POST['participant'])
    curr_trip = Trip.objects.get(id=trip_id)
    if user_added in curr_trip.users_joined.all():
        curr_trip.users_joined.remove(user_added)
    else:
        curr_trip.users_joined.add(user_added)
    return redirect(f'/dashboard/trips/{trip_id}')

def add_remove_friend(request, friend_id):
    friend_added = User.objects.get(id=friend_id)
    curr_user = User.objects.get(id=request.session['user_id'])
    if friend_added in curr_user.friends.all():
        curr_user.friends.remove(friend_added)
    else:
        curr_user.friends.add(friend_added)
    return redirect('/dashboard/friends')

def add_activity(request, trip_id):
    errors = Itinerary.objects.itinerary_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/dashboard/trips/{trip_id}/itinerary')
    else:
        curr_trip = Trip.objects.get(id=trip_id)
        new_activity = Itinerary.objects.create(date=request.POST['date'], start_time=request.POST['start_time'], end_time=request.POST['end_time'], activity=request.POST['activity'], address=request.POST['address'], notes=request.POST['notes'], trip=curr_trip)
        messages.success(request, "New Activity has been added.")
        return redirect(f'/dashboard/trips/{trip_id}/itinerary')

def edit_activity(request, trip_id, itinerary_id):
    if 'cancel' in request.POST:
        return redirect(f'/dashboard/trips/{trip_id}/itinerary/')
    errors = Itinerary.objects.itinerary_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/dashboard/trips/{trip_id}/itinerary/{itinerary_id}')
    else:
        curr_activity = Itinerary.objects.get(id=itinerary_id)
        curr_activity.date = request.POST['date']
        curr_activity.start_time = request.POST['start_time']
        curr_activity.end_time = request.POST['end_time']
        curr_activity.activity = request.POST['activity']
        curr_activity.address = request.POST['address']
        curr_activity.notes = request.POST['notes']
        curr_activity.save()
        messages.success(request, f"Activity #{itinerary_id} has been updated.")
        return redirect(f'/dashboard/trips/{trip_id}/itinerary')

def remove_activity(request, trip_id, activity_id):
    curr_activity = Itinerary.objects.get(id=activity_id)
    curr_activity.delete()
    return redirect(f'/dashboard/trips/{trip_id}/itinerary')

def add_expense(request, trip_id):
    errors = Expense.objects.expense_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/dashboard/trips/{trip_id}/expense')
    else:
        curr_trip = Trip.objects.get(id=trip_id)
        new_expense = Expense.objects.create(amount=request.POST['amount'], paid_by=User.objects.get(id=request.POST['paid_by']), notes=request.POST['notes'], trip=curr_trip)
        messages.success(request, "New Expense has been added.")
        return redirect(f'/dashboard/trips/{trip_id}/expense')

def edit_expense(request, trip_id, expense_id):
    if 'cancel' in request.POST:
        return redirect(f'/dashboard/trips/{trip_id}/expense')
    errors = Expense.objects.expense_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/dashboard/trips/{trip_id}/expense/{expense_id}')
    else:
        curr_expense = Expense.objects.get(id=expense_id)
        curr_expense.amount = request.POST['amount']
        curr_expense.paid_by = User.objects.get(id=request.POST['paid_by'])
        curr_expense.notes = request.POST['notes']
        curr_expense.save()
        messages.success(request, f"Activity #{expense_id} has been updated.")
        return redirect(f'/dashboard/trips/{trip_id}/expense')

def remove_expense(request, trip_id, expense_id):
    curr_expense = Expense.objects.get(id=expense_id)
    curr_expense.delete()
    return redirect(f'/dashboard/trips/{trip_id}/expense')
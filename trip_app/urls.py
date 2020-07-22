from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_dashboard),
    path('/trips', views.trip_dashboard),
    path('/trips/<int:trip_id>', views.view_dashboard),
    path('/trips/edit/<int:trip_id>', views.edit_dashboard),
    path('/trips/edit/<int:trip_id>/process', views.edit_trip),
    path('/trips/<int:trip_id>/remove', views.remove_trip),
    path('/trips/new', views.add_dashboard),
    path('/trips/new/process', views.add_trip),
    path('/trips/<int:trip_id>/leave', views.leave_trip),
    path('/trips/<int:trip_id>/participate', views.add_remove_participant),
    path('/friends', views.friends_dashboard),
    path('/friends/<int:friend_id>', views.add_remove_friend),
    path('/trips/<int:trip_id>/itinerary', views.itinerary_dashboard),
    path('/trips/<int:trip_id>/itinerary/new', views.add_activity),
    path('/trips/<int:trip_id>/itinerary/<int:itinerary_id>', views.edit_activity_dashboard),
    path('/trips/<int:trip_id>/itinerary/<int:itinerary_id>/edit', views.edit_activity),
    path('/trips/<int:trip_id>/itinerary/<int:itinerary_id>/remove', views.remove_activity),
    path('/trips/<int:trip_id>/expense', views.expense_log),
    path('/trips/<int:trip_id>/expense/new', views.add_expense),
    path('/trips/<int:trip_id>/expense/<int:expense_id>', views.edit_expense_dashboard),
    path('/trips/<int:trip_id>/expense/<int:expense_id>/edit', views.edit_expense),
    path('/trips/<int:trip_id>/expense/<int:expense_id>/remove', views.remove_expense),
]
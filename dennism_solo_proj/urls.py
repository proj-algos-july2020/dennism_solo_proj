from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from login_register_app.models import User
from trip_app.models import Trip, Itinerary, Expense, PhotoAlbum

class UserAdmin(admin.ModelAdmin):
    pass
admin.site.register(User,UserAdmin)

class TripAdmin(admin.ModelAdmin):
    pass
admin.site.register(Trip,TripAdmin)

class ItineraryAdmin(admin.ModelAdmin):
    pass
admin.site.register(Itinerary,ItineraryAdmin)

class ExpenseAdmin(admin.ModelAdmin):
    pass
admin.site.register(Expense,ExpenseAdmin)

class PhotoAlbumAdmin(admin.ModelAdmin):
    pass
admin.site.register(PhotoAlbum,PhotoAlbumAdmin)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('login_register_app.urls')),
    path('dashboard/', include('trip_app.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.contrib import admin
from . models import SearchCategory, Destination, Booking

# Register your models here.
admin.site.register(SearchCategory)
admin.site.register(Destination)
admin.site.register(Booking)
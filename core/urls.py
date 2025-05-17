from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
    path('index/', views.IndexView.as_view(), name='index'),
    path('search/<int:category_id>/', views.search_results, name='search_results'),
    path('booking/confirmation/<int:booking_id>/', views.booking_confirmation, name='booking_confirmation'),
    # Add other URL patterns as needed
]

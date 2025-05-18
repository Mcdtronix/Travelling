from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('search/<int:category_id>/', views.search_results, name='search_results'),
    path('booking/<int:booking_id>/', views.booking_confirmation, name='booking_confirmation'),
    path('offers/', views.OffersView.as_view(), name='offers'),
    path('destination/<slug:slug>/', views.destination_detail, name='destination_detail'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('blog/', views.BlogView.as_view(), name='blog'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    # Add other URL patterns as needed
]

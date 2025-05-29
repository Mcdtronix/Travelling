from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('offers/', views.OffersView.as_view(), name='offers'),
    path('destination/<slug:slug>/', views.DestinationDetailView.as_view(), name='destination_detail'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('blog/', views.BlogView.as_view(), name='blog'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('activities/', views.ActivityView.as_view(), name='activities'),
    path('contact/submit/', views.contact_form_submit, name='contact_form_submit'),
    path('elements/', views.ElementsView.as_view(), name='elements'),
    path('listing/<slug:slug>/', views.ListingDetailView.as_view(), name='listing_detail'),
    path('booking/create/', views.create_booking, name='create_booking'),
    # Add other URL patterns as needed
]

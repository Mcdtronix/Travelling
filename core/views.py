from django.shortcuts import render, get_object_or_404

from django.shortcuts import render
from .models import SearchCategory, Destination, Booking
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime


# Create your views here.



class IndexView(TemplateView):
    template_name = 'index.html'

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get all search categories ordered by their defined order
        context['search_categories'] = SearchCategory.objects.all()
        
        # Get all destinations for the autocomplete
        context['destinations'] = Destination.objects.all()
        
        # Range for adults dropdown (1-10)
        context['adults_range'] = range(1, 11)
        
        # Range for children dropdown (0-6)
        context['children_range'] = range(0, 7)
        
        return context

def search_results(request, category_id):
    """Handle search form submissions"""
    if request.method == 'POST':
        # Get the category
        category = SearchCategory.objects.get(id=category_id)
        
        # Process the form data
        destination_input = request.POST.get('destination', '')
        check_in = request.POST.get('check_in')
        check_out = request.POST.get('check_out')
        adults = request.POST.get('adults')
        children = request.POST.get('children')
        
        # Parse destination input (format: "City, Country")
        try:
            city, country = destination_input.split(',', 1)
            city = city.strip()
            country = country.strip()
            
            # Get or create the destination
            destination, created = Destination.objects.get_or_create(
                name=city,
                country=country
            )
            
            # Create a new booking record
            booking = Booking.objects.create(
                category=category,
                destination=destination,
                check_in_date=check_in,
                check_out_date=check_out,
                adults=adults,
                children=children
            )
            
            # Redirect to a success page or search results page
            return HttpResponseRedirect(reverse('booking_confirmation', args=[booking.id]))
            
        except ValueError:
            # Handle invalid destination format
            # This is a simplified error handling, you might want to add more robust validation
            pass
            
    # If not a POST request or there was an error, redirect back to the index
    return HttpResponseRedirect(reverse('index'))

def booking_confirmation(request, booking_id):
    """Display booking confirmation page"""
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, 'booking_confirmation.html', {
        'booking': booking
    })
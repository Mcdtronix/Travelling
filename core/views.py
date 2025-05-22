from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, ListView, DetailView
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib import messages
from .models import (
    SearchCategory, 
    Destination, 
    Booking, 
    FeaturedDestination,
    SpecialOffer,
    TrendingPlace,
    Testimonial,
    BlogPost,
    ContactInfo,
    ContactFormSubmission,
    Activity,
    Listing
)
import datetime


# Create your views here.



class IndexView(TemplateView):
    template_name = 'index.html'

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get all search categories ordered by their defined order
        context['search_categories'] = SearchCategory.objects.filter(is_active=True)
        
        # Get all destinations for the autocomplete
        context['destinations'] = Destination.objects.all()
        
        # Range for adults dropdown (1-10)
        context['adults_range'] = range(1, 11)
        
        # Range for children dropdown (0-6)
        context['children_range'] = range(0, 7)

        # Featured destinations for slider
        context['featured_destinations'] = FeaturedDestination.objects.filter(is_active=True)

        # Special offers
        context['special_offers'] = SpecialOffer.objects.filter(
            is_active=True,
            end_date__gte=datetime.date.today()
        )[:3]  # Show only 3 offers

        # Trending places
        context['trending_places'] = TrendingPlace.objects.filter(is_active=True)[:8]

        # Activities for slider - ordered by order field and limited to 6
        context['activities'] = Activity.objects.filter(
            is_active=True
        ).order_by('order', '-rating').distinct()[:6]

        # Testimonials
        context['testimonials'] = Testimonial.objects.filter(is_active=True)[:6]

        # Recent blog posts
        context['recent_blog_posts'] = BlogPost.objects.filter(is_active=True)[:3]

        # Contact information
        try:
            context['contact_info'] = ContactInfo.objects.first()
        except ContactInfo.DoesNotExist:
            context['contact_info'] = None
        
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

class OffersView(ListView):
    template_name = 'offers.html'
    model = SpecialOffer
    context_object_name = 'special_offers'

    def get_queryset(self):
        return SpecialOffer.objects.filter(
            is_active=True,
            end_date__gte=datetime.date.today()
        ).select_related('destination')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add contact info for the header
        try:
            context['contact_info'] = ContactInfo.objects.first()
        except ContactInfo.DoesNotExist:
            context['contact_info'] = None
        return context

class DestinationDetailView(DetailView):
    model = Destination
    template_name = 'destination_detail.html'
    context_object_name = 'destination'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        destination = self.get_object()
        
        # Get special offers for this destination
        context['special_offers'] = SpecialOffer.objects.filter(
            destination=destination,
            is_active=True,
            end_date__gte=datetime.date.today()
        )

        # Get contact info for the header
        try:
            context['contact_info'] = ContactInfo.objects.first()
        except ContactInfo.DoesNotExist:
            context['contact_info'] = None

        return context

# Update the URL pattern to use this class-based view
destination_detail = DestinationDetailView.as_view()

class AboutView(TemplateView):
    template_name = 'about.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['contact_info'] = ContactInfo.objects.first()
        except ContactInfo.DoesNotExist:
            context['contact_info'] = None
        return context

class BlogView(ListView):
    template_name = 'blog.html'
    model = BlogPost
    context_object_name = 'blog_posts'
    
    def get_queryset(self):
        return BlogPost.objects.filter(is_active=True).order_by('-publish_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['contact_info'] = ContactInfo.objects.first()
        except ContactInfo.DoesNotExist:
            context['contact_info'] = None
        return context

class ContactView(TemplateView):
    template_name = 'contact.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['contact_info'] = ContactInfo.objects.first()
        except ContactInfo.DoesNotExist:
            context['contact_info'] = None
        return context

class ElementsView(TemplateView):
    template_name = 'elements.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['contact_info'] = ContactInfo.objects.first()
        except ContactInfo.DoesNotExist:
            context['contact_info'] = None
        return context

class ActivityView(ListView):
    template_name = 'activities.html'
    model = Activity
    context_object_name = 'activities'
    
    def get_queryset(self):
        return Activity.objects.filter(is_active=True).order_by('order')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['contact_info'] = ContactInfo.objects.first()
        except ContactInfo.DoesNotExist:
            context['contact_info'] = None
        return context

def contact_form_submit(request):
    """Handle contact form submissions"""
    if request.method == 'POST':
        try:
            # Get form data
            name = request.POST.get('name')
            email = request.POST.get('email')
            subject = request.POST.get('subject')
            message = request.POST.get('message')

            # Create new submission
            submission = ContactFormSubmission.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message
            )

            # Return success response
            return JsonResponse({
                'status': 'success',
                'message': 'Thank you for your message. We will get back to you soon!'
            })
        except Exception as e:
            # Return error response
            return JsonResponse({
                'status': 'error',
                'message': 'Sorry, there was an error sending your message. Please try again.'
            })
    
    # If not POST request, redirect to home
    return redirect('index')

class ListingDetailView(TemplateView):
    template_name = 'listing.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = kwargs.get('slug')
        
        # Get the listing details
        listing = get_object_or_404(Listing, slug=slug)
        context['listing'] = listing
        
        # Get related listings
        context['related_listings'] = Listing.objects.filter(
            destination=listing.destination
        ).exclude(id=listing.id)[:3]
        
        # Get destination details
        context['destination'] = listing.destination
        
        # Get available dates
        context['available_dates'] = listing.get_available_dates()
        
        return context 
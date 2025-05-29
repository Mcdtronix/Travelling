from django.contrib import admin
from django.utils.text import slugify
from .models import (
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

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'base_price', 'rating', 'slug')
    list_filter = ('country', 'rating')
    search_fields = ('name', 'country', 'description')
    prepopulated_fields = {'slug': ('name',)}

    def save_model(self, request, obj, form, change):
        if not obj.slug:
            obj.slug = slugify(obj.name)
        super().save_model(request, obj, form, change)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('destination', 'check_in_date', 'check_out_date', 'adults', 'children')
    list_filter = ('check_in_date', 'destination')
    search_fields = ('destination__name',)
    date_hierarchy = 'check_in_date'

@admin.register(FeaturedDestination)
class FeaturedDestinationAdmin(admin.ModelAdmin):
    list_display = ('title', 'destination', 'is_active', 'button_text')
    list_filter = ('is_active', 'destination')
    search_fields = ('title', 'subtitle', 'destination__name')
    raw_id_fields = ('destination',)

@admin.register(SpecialOffer)
class SpecialOfferAdmin(admin.ModelAdmin):
    list_display = ('title', 'destination', 'price', 'discount_percentage', 'start_date', 'end_date', 'is_active')
    list_filter = ('is_active', 'destination', 'start_date', 'end_date')
    search_fields = ('title', 'description', 'destination__name')
    date_hierarchy = 'start_date'
    raw_id_fields = ('destination',)

@admin.register(TrendingPlace)
class TrendingPlaceAdmin(admin.ModelAdmin):
    list_display = ('destination', 'price_from', 'is_active')
    list_filter = ('is_active', 'destination')
    search_fields = ('destination__name',)
    raw_id_fields = ('destination',)

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'rating', 'date', 'is_active')
    list_filter = ('rating', 'is_active', 'date')
    search_fields = ('client_name', 'content')
    date_hierarchy = 'date'

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publish_date', 'is_active')
    list_filter = ('is_active', 'publish_date', 'author')
    search_fields = ('title', 'content', 'author')
    date_hierarchy = 'publish_date'
    prepopulated_fields = {'slug': ('title',)}

@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ('phone', 'email', 'address')

    def has_add_permission(self, request):
        # Only allow one ContactInfo instance
        if self.model.objects.exists():
            return False
        return True

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'price', 'duration', 'rating', 'is_active', 'order')
    list_filter = ('is_active', 'rating', 'location')
    search_fields = ('title', 'description', 'location')
    list_editable = ('is_active', 'order', 'price', 'rating')
    ordering = ('order', '-rating')
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'image')
        }),
        ('Details', {
            'fields': ('price', 'duration', 'location', 'rating')
        }),
        ('Settings', {
            'fields': ('is_active', 'order')
        }),
    )

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'destination', 'price', 'rating', 'is_active')
    list_filter = ('is_active', 'destination', 'rating')
    search_fields = ('title', 'description', 'destination__name')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('destination',)
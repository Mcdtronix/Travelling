from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify
from django.utils import timezone
from django.core.exceptions import ValidationError



class Destination(models.Model):
    """Model for travel destinations"""
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    is_popular = models.BooleanField(default=False)
    image = models.ImageField(upload_to='destinations/', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=4
    )
    base_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.name}-{self.country}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}, {self.country}"

class Booking(models.Model):
    """Model for bookings across all categories"""
    BOOKING_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]

    name = models.CharField(max_length=200, default='Name')
    email = models.EmailField(max_length=254, null=True, blank=True)
    contact = models.CharField(max_length=20, null=True, blank=True)  # Changed to CharField for better phone validation
    destination = models.ForeignKey('Destination', on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    adults = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    children = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, choices=BOOKING_STATUS_CHOICES, default='pending')
    special_requests = models.TextField(blank=True, null=True, help_text="Any special requirements")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'

    def clean(self):
        """Custom validation for booking dates"""
        if self.check_in_date and self.check_out_date:
            if self.check_in_date < timezone.now().date():
                raise ValidationError("Check-in date cannot be in the past.")
            if self.check_out_date <= self.check_in_date:
                raise ValidationError("Check-out date must be after check-in date.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    @property
    def total_guests(self):
        return self.adults + self.children

    @property
    def duration_days(self):
        if self.check_in_date and self.check_out_date:
            return (self.check_out_date - self.check_in_date).days
        return 0

    def __str__(self):
        return f"{self.name} - {self.destination} ({self.check_in_date} to {self.check_out_date})"



class FeaturedDestination(models.Model):
    """Model for featured destinations in the home slider"""
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    listing = models.ForeignKey('Listing', on_delete=models.SET_NULL, null=True, blank=True, related_name='featured_destinations')
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200)
    background_image = models.ImageField(upload_to='featured/')
    button_text = models.CharField(max_length=50, default='explore now')
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Featured: {self.destination.name}"

class SpecialOffer(models.Model):
    """Model for special offers section"""
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percentage = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=0
    )
    start_date = models.DateField()
    end_date = models.DateField()
    image = models.ImageField(upload_to='offers/')
    description = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} - {self.destination.name}"

class TrendingPlace(models.Model):
    """Model for trending places section"""
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='trending/')
    price_from = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Trending: {self.destination.name}"

class Testimonial(models.Model):
    """Model for client testimonials"""
    client_name = models.CharField(max_length=100)
    client_photo = models.ImageField(upload_to='testimonials/')
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=5
    )
    comment = models.TextField()
    date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Testimonial by {self.client_name}"

class Activity(models.Model):
    """Model for travel activities"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='activities/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.CharField(max_length=50)  # e.g., "2 hours", "Full day"
    location = models.CharField(max_length=200)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=5
    )
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)  # For ordering in the slider

    class Meta:
        verbose_name_plural = "Activities"
        ordering = ['order']

    def __str__(self):
        return self.title

class BlogPost(models.Model):
    """Model for blog posts"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    content = models.TextField()
    image = models.ImageField(upload_to='blog/')
    author = models.CharField(max_length=100)
    publish_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-publish_date']

    def __str__(self):
        return self.title

class ContactInfo(models.Model):
    """Model for contact information"""
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    website = models.URLField()
    facebook = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    pinterest = models.URLField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Contact Information"

    def __str__(self):
        return "Contact Information"

class ContactFormSubmission(models.Model):
    """Model for contact form submissions"""
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-submitted_at']

    def __str__(self):
        return f"Message from {self.name} - {self.subject}"

class Listing(models.Model):
    """Model for property listings"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='listings/')
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=5
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_available_dates(self):
        # This is a placeholder method - implement actual availability logic
        return []

    def __str__(self):
        return self.title
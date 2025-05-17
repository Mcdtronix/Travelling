from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify

# Create your models here.
class SearchCategory(models.Model):
    """Model for search categories (hotels, car rentals, flights, etc.)"""
    name = models.CharField(max_length=50)
    icon = models.CharField(max_length=100, null=True, blank=True )  # Path to the icon image
    is_active = models.BooleanField(default=False)
    order = models.IntegerField(default=0)  # For ordering tabs
    
    class Meta:
        verbose_name_plural = "Search Categories"
        ordering = ['order']
        
    def __str__(self):
        return self.name

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
    category = models.ForeignKey(SearchCategory, on_delete=models.CASCADE)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    adults = models.PositiveIntegerField(default=1)
    children = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.category.name} booking for {self.destination} ({self.check_in_date} to {self.check_out_date})"

class FeaturedDestination(models.Model):
    """Model for featured destinations in the home slider"""
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
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
from django.db import models

# Create your models here.
class SearchCategory(models.Model):
    """Model for search categories (hotels, car rentals, flights, etc.)"""
    name = models.CharField(max_length=50)
    icon = models.CharField(max_length=100)  # Path to the icon image
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
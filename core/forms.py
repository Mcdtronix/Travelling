from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Booking, Destination
import re

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['name', 'email', 'contact', 'destination', 'check_in_date',
                 'check_out_date', 'adults', 'children', 'special_requests']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Full Name',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email Address',
                'required': True
            }),
            'contact': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone Number',
                'required': True
            }),
            'destination': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'check_in_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': True
            }),
            'check_out_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': True
            }),
            'adults': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '10',
                'value': '1'
            }),
            'children': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '10',
                'value': '0'
            }),
            'special_requests': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Any special requirements or requests...'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set queryset for destinations to only active ones if you have such field
        self.fields['destination'].queryset = Destination.objects.all()
        self.fields['destination'].empty_label = "Select Destination"

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            raise ValidationError("Name is required.")
        if len(name.strip()) < 2:
            raise ValidationError("Name must be at least 2 characters long.")
        if not re.match("^[a-zA-Z\s]+$", name):
            raise ValidationError("Name should only contain letters and spaces.")
        return name.strip().title()

    def clean_contact(self):
        contact = self.cleaned_data.get('contact')
        if not contact:
            raise ValidationError("Phone number is required.")

        # Remove any non-digit characters except + at the beginning
        cleaned_contact = re.sub(r'[^\d+]', '', contact)

        # Check if it starts with + and has appropriate length
        if cleaned_contact.startswith('+'):
            if len(cleaned_contact) < 10 or len(cleaned_contact) > 15:
                raise ValidationError("Invalid phone number format.")
        else:
            if len(cleaned_contact) < 9 or len(cleaned_contact) > 15:
                raise ValidationError("Invalid phone number format.")

        return cleaned_contact

    def clean_check_in_date(self):
        check_in_date = self.cleaned_data.get('check_in_date')
        if check_in_date:
            if check_in_date < timezone.now().date():
                raise ValidationError("Check-in date cannot be in the past.")
        return check_in_date

    def clean_check_out_date(self):
        check_out_date = self.cleaned_data.get('check_out_date')
        check_in_date = self.cleaned_data.get('check_in_date')

        if check_out_date and check_in_date:
            if check_out_date <= check_in_date:
                raise ValidationError("Check-out date must be after check-in date.")

            # Optional: Limit booking duration (e.g., maximum 30 days)
            duration = (check_out_date - check_in_date).days
            if duration > 30:
                raise ValidationError("Booking duration cannot exceed 30 days.")

        return check_out_date

    def clean_adults(self):
        adults = self.cleaned_data.get('adults')
        if adults is not None and adults < 1:
            raise ValidationError("At least 1 adult is required.")
        if adults is not None and adults > 10:
            raise ValidationError("Maximum 10 adults allowed.")
        return adults

    def clean_children(self):
        children = self.cleaned_data.get('children')
        if children is not None and children < 0:
            raise ValidationError("Number of children cannot be negative.")
        if children is not None and children > 10:
            raise ValidationError("Maximum 10 children allowed.")
        return children

    def clean(self):
        cleaned_data = super().clean()
        adults = cleaned_data.get('adults', 0)
        children = cleaned_data.get('children', 0)

        total_guests = adults + children
        if total_guests > 12:
            raise ValidationError("Total number of guests cannot exceed 12.")

        return cleaned_data

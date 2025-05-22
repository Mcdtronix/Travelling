from django.core.management.base import BaseCommand
from core.models import SearchCategory, Destination

class Command(BaseCommand):
    help = 'Sets up initial data for the travel website'

    def handle(self, *args, **kwargs):
        # Create search categories
        categories = [
            {
                'name': 'Hotels',
                'icon': 'images/hotel.png',
                'is_active': True,
                'order': 1
            },
            {
                'name': 'Flights',
                'icon': 'images/airplane.png',
                'is_active': True,
                'order': 2
            },
            {
                'name': 'Car Rentals',
                'icon': 'images/car.png',
                'is_active': True,
                'order': 3
            },
            {
                'name': 'Cruises',
                'icon': 'images/cruise.png',
                'is_active': True,
                'order': 4
            }
        ]

        # Create destinations
        destinations = [
            {'name': 'Paris', 'country': 'France', 'is_popular': True},
            {'name': 'London', 'country': 'United Kingdom', 'is_popular': True},
            {'name': 'New York', 'country': 'United States', 'is_popular': True},
            {'name': 'Tokyo', 'country': 'Japan', 'is_popular': True},
            {'name': 'Rome', 'country': 'Italy', 'is_popular': True},
        ]

        for category_data in categories:
            SearchCategory.objects.get_or_create(
                name=category_data['name'],
                defaults={
                    'icon': category_data['icon'],
                    'is_active': category_data['is_active'],
                    'order': category_data['order']
                }
            )
            self.stdout.write(f"Created category: {category_data['name']}")

        for dest_data in destinations:
            Destination.objects.get_or_create(
                name=dest_data['name'],
                country=dest_data['country'],
                defaults={'is_popular': dest_data['is_popular']}
            )
            self.stdout.write(f"Created destination: {dest_data['name']}, {dest_data['country']}")

        self.stdout.write(self.style.SUCCESS('Successfully set up initial data')) 
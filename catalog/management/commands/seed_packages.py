"""
Management command để seed packages vào database
Chạy: python manage.py seed_packages
"""
from django.core.management.base import BaseCommand
from catalog.models import Package, Destination
from tours.models import Tour
from hotels.models import Hotel
from flight.models import Flight
from django.utils import timezone


class Command(BaseCommand):
    help = 'Seed packages vào database với đầy đủ thông tin'

    def handle(self, *args, **options):
        self.stdout.write('Starting to seed packages...')
        
        # Tạo hoặc lấy destinations
        destinations_data = [
            {'name': 'Ha Long Bay', 'slug': 'ha-long-bay', 'country': 'Vietnam', 'region': 'Quang Ninh'},
            {'name': 'Da Nang', 'slug': 'da-nang', 'country': 'Vietnam', 'region': 'Da Nang'},
            {'name': 'Sapa', 'slug': 'sapa', 'country': 'Vietnam', 'region': 'Lao Cai'},
            {'name': 'Phu Quoc', 'slug': 'phu-quoc', 'country': 'Vietnam', 'region': 'Kien Giang'},
            {'name': 'Nha Trang', 'slug': 'nha-trang', 'country': 'Vietnam', 'region': 'Khanh Hoa'},
        ]
        
        destinations = {}
        for dest_data in destinations_data:
            dest, created = Destination.objects.get_or_create(
                slug=dest_data['slug'],
                defaults={
                    'name': dest_data['name'],
                    'country': dest_data['country'],
                    'region': dest_data['region'],
                    'is_active': True,
                }
            )
            destinations[dest_data['slug']] = dest
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created destination: {dest.name}'))
            else:
                self.stdout.write(f'  Destination already exists: {dest.name}')
        
        # Packages data với đầy đủ thông tin
        packages_data = [
            {
                'id': 1,
                'title': 'Combo Ha Long 3N2Đ',
                'destination_slug': 'ha-long-bay',
                'description': 'Tour + khách sạn + flight nội địa',
                'base_price': 6500000,
                'label': 'family',
                'tour_ids': [1001],
                'hotel_ids': [2001],
                'flight_ids': [3001],
            },
            {
                'id': 2,
                'title': 'Combo Da Nang 2N1Đ',
                'destination_slug': 'da-nang',
                'description': 'City tour + hotel trung tâm + flight',
                'base_price': 3200000,
                'label': 'couple',
                'tour_ids': [1002],
                'hotel_ids': [2002],
                'flight_ids': [3002],
            },
            {
                'id': 3,
                'title': 'Combo Sapa Trekking 2N1Đ',
                'destination_slug': 'sapa',
                'description': 'Trekking Fansipan + homestay',
                'base_price': 2500000,
                'label': 'adventure',
                'tour_ids': [1003],
                'hotel_ids': [],
                'flight_ids': [],
            },
            {
                'id': 4,
                'title': 'Combo Phú Quốc Resort 4N3Đ',
                'destination_slug': 'phu-quoc',
                'description': 'Resort 5 sao + tour đảo',
                'base_price': 6500000,
                'label': 'luxury',
                'tour_ids': [1004],
                'hotel_ids': [],
                'flight_ids': [],
            },
            {
                'id': 5,
                'title': 'Combo Nha Trang Beach 3N2Đ',
                'destination_slug': 'nha-trang',
                'description': 'Biển xanh và hải sản tươi',
                'base_price': 4200000,
                'label': 'family',
                'tour_ids': [1005],
                'hotel_ids': [],
                'flight_ids': [],
            },
        ]
        
        created_count = 0
        updated_count = 0
        
        for pkg_data in packages_data:
            destination = destinations.get(pkg_data['destination_slug'])
            if not destination:
                self.stdout.write(self.style.WARNING(f'Warning: Destination not found: {pkg_data["destination_slug"]}'))
                continue
            
            package, created = Package.objects.get_or_create(
                id=pkg_data['id'],
                defaults={
                    'title': pkg_data['title'],
                    'destination': destination,
                    'description': pkg_data['description'],
                    'base_price': pkg_data['base_price'],
                    'label': pkg_data['label'],
                    'is_active': True,
                }
            )
            
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'Created package: {package.title} (ID: {package.id})'))
            else:
                # Update package if already exists
                package.title = pkg_data['title']
                package.destination = destination
                package.description = pkg_data['description']
                package.base_price = pkg_data['base_price']
                package.label = pkg_data['label']
                package.is_active = True
                package.save()
                updated_count += 1
                self.stdout.write(f'  Updated package: {package.title} (ID: {package.id})')
            
            # Thêm tours
            for tour_id in pkg_data.get('tour_ids', []):
                try:
                    tour = Tour.objects.get(tour_id=tour_id)
                    package.tours.add(tour)
                except Tour.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f'  Warning: Tour {tour_id} not found'))
            
            # Add hotels
            for hotel_id in pkg_data.get('hotel_ids', []):
                try:
                    hotel = Hotel.objects.get(hotel_id=hotel_id)
                    package.hotels.add(hotel)
                except Hotel.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f'  Warning: Hotel {hotel_id} not found'))
            
            # Add flights
            for flight_id in pkg_data.get('flight_ids', []):
                try:
                    flight = Flight.objects.get(flight_id=flight_id)
                    package.flights.add(flight)
                except Flight.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f'  Warning: Flight {flight_id} not found'))
        
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(f'Completed! Created {created_count} packages, updated {updated_count} packages'))
        self.stdout.write(f'  Total active packages: {Package.objects.filter(is_active=True).count()}')


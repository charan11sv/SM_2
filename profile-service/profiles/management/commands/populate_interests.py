from django.core.management.base import BaseCommand
from interests.models import Interest


class Command(BaseCommand):
    help = 'Populate initial interests data'
    
    def handle(self, *args, **options):
        """Populate interests with predefined data"""
        
        interests_data = [
            # Technology
            {'name': 'Programming', 'category': 'technology', 'description': 'Software development and coding'},
            {'name': 'Artificial Intelligence', 'category': 'technology', 'description': 'AI and machine learning'},
            {'name': 'Web Development', 'category': 'technology', 'description': 'Building websites and web applications'},
            {'name': 'Mobile Apps', 'category': 'technology', 'description': 'Mobile application development'},
            {'name': 'Cybersecurity', 'category': 'technology', 'description': 'Digital security and privacy'},
            
            # Sports
            {'name': 'Football', 'category': 'sports', 'description': 'Soccer and football games'},
            {'name': 'Basketball', 'category': 'sports', 'description': 'Basketball games and tournaments'},
            {'name': 'Tennis', 'category': 'sports', 'description': 'Tennis matches and training'},
            {'name': 'Swimming', 'category': 'sports', 'description': 'Swimming and water sports'},
            {'name': 'Running', 'category': 'sports', 'description': 'Running and marathons'},
            
            # Music
            {'name': 'Rock', 'category': 'music', 'description': 'Rock music and bands'},
            {'name': 'Jazz', 'category': 'music', 'description': 'Jazz music and improvisation'},
            {'name': 'Classical', 'category': 'music', 'description': 'Classical music and orchestras'},
            {'name': 'Pop', 'category': 'music', 'description': 'Popular music and hits'},
            {'name': 'Hip Hop', 'category': 'music', 'description': 'Hip hop and rap music'},
            
            # Travel
            {'name': 'Backpacking', 'category': 'travel', 'description': 'Budget travel and backpacking'},
            {'name': 'Luxury Travel', 'category': 'travel', 'description': 'Premium travel experiences'},
            {'name': 'Adventure Travel', 'category': 'travel', 'description': 'Extreme and adventure tourism'},
            {'name': 'Cultural Tourism', 'category': 'travel', 'description': 'Cultural and heritage tourism'},
            {'name': 'Beach Vacations', 'category': 'travel', 'description': 'Beach and coastal holidays'},
            
            # Food & Cooking
            {'name': 'Baking', 'category': 'food', 'description': 'Baking breads and pastries'},
            {'name': 'Cooking', 'category': 'food', 'description': 'General cooking and recipes'},
            {'name': 'Wine Tasting', 'category': 'food', 'description': 'Wine appreciation and tasting'},
            {'name': 'Food Photography', 'category': 'food', 'description': 'Photographing food and dishes'},
            {'name': 'International Cuisine', 'category': 'food', 'description': 'Exploring world cuisines'},
            
            # Art & Design
            {'name': 'Painting', 'category': 'art', 'description': 'Painting and visual arts'},
            {'name': 'Digital Art', 'category': 'art', 'description': 'Digital artwork and design'},
            {'name': 'Photography', 'category': 'art', 'description': 'Photography and image capture'},
            {'name': 'Graphic Design', 'category': 'art', 'description': 'Graphic design and branding'},
            {'name': 'Sculpture', 'category': 'art', 'description': '3D art and sculpture'},
            
            # Fashion
            {'name': 'Street Style', 'category': 'fashion', 'description': 'Urban and street fashion'},
            {'name': 'Sustainable Fashion', 'category': 'fashion', 'description': 'Eco-friendly fashion choices'},
            {'name': 'Vintage Fashion', 'category': 'fashion', 'description': 'Retro and vintage clothing'},
            {'name': 'Fashion Photography', 'category': 'fashion', 'description': 'Fashion and style photography'},
            {'name': 'Accessories', 'category': 'fashion', 'description': 'Jewelry and fashion accessories'},
            
            # Gaming
            {'name': 'PC Gaming', 'category': 'gaming', 'description': 'Computer and PC games'},
            {'name': 'Console Gaming', 'category': 'gaming', 'description': 'Video game consoles'},
            {'name': 'Mobile Gaming', 'category': 'gaming', 'description': 'Mobile and smartphone games'},
            {'name': 'Esports', 'category': 'gaming', 'description': 'Competitive gaming and tournaments'},
            {'name': 'Board Games', 'category': 'gaming', 'description': 'Tabletop and board games'},
            
            # Fitness & Health
            {'name': 'Yoga', 'category': 'fitness', 'description': 'Yoga and meditation'},
            {'name': 'Weight Training', 'category': 'fitness', 'description': 'Strength training and bodybuilding'},
            {'name': 'Cardio', 'category': 'fitness', 'description': 'Cardiovascular exercises'},
            {'name': 'Nutrition', 'category': 'fitness', 'description': 'Healthy eating and diet'},
            {'name': 'Mental Health', 'category': 'fitness', 'description': 'Mental wellness and psychology'},
        ]
        
        created_count = 0
        updated_count = 0
        
        for interest_data in interests_data:
            interest, created = Interest.objects.get_or_create(
                name=interest_data['name'],
                defaults={
                    'category': interest_data['category'],
                    'description': interest_data['description'],
                    'is_active': True
                }
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created interest: {interest.name}')
                )
            else:
                # Update existing interest
                interest.category = interest_data['category']
                interest.description = interest_data['description']
                interest.is_active = True
                interest.save()
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(f'Updated interest: {interest.name}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully processed interests. '
                f'Created: {created_count}, Updated: {updated_count}'
            )
        )

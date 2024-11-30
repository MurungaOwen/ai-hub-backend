from django.core.management.base import BaseCommand
from forums.models import Forum

class Command(BaseCommand):
    help = 'Creates 4 forums if they don\'t exist'

    def handle(self, *args, **kwargs):
        forums_data = [
            {'title': 'AI and Machine Learning', 'description': 'A forum for AI and machine learning discussions.'},
            {'title': 'Neural Networks', 'description': 'A forum for discussions on neural networks.'},
            {'title': 'Deep Learning', 'description': 'A forum for deep learning research and conversations.'},
            {'title': 'AI Ethics', 'description': 'A forum to discuss ethical concerns in AI development.'},
        ]

        for forum_data in forums_data:
            # Check if a forum with the same title exists
            if not Forum.objects.filter(title=forum_data['title']).exists():
                Forum.objects.create(**forum_data)
                self.stdout.write(self.style.SUCCESS(f"Forum '{forum_data['title']}' created successfully."))
            else:
                self.stdout.write(self.style.WARNING(f"Forum '{forum_data['title']}' already exists."))


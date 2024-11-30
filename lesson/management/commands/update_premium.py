from django.core.management.base import BaseCommand
from django.utils import timezone
from lesson.models import CustomUser

class Command(BaseCommand):
    help = 'Updates premium status for users whose premium expiry date has passed'

    def handle(self, *args, **kwargs):

        now = timezone.now()

        # Perform the update in the database
        users = CustomUser.objects.filter(premium_expiry__lt=now, is_premium=True)

        updated_count = 0
        for user in users:
            user.is_premium = False
            user.save()
            updated_count += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully updated {updated_count} users to non-premium.'))

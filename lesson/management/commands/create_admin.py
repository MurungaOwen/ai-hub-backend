from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from decouple import config

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates an admin user if one does not exist.'

    def handle(self, *args, **kwargs):
        admin_username = config('ADMIN_USERNAME', 'admin') # provide default if not provided
        admin_email = config('ADMIN_EMAIL', 'admin@mail.com')
        admin_password = config('ADMIN_PASSWORD', 'admin')

        # Check if the admin user already exists
        if not User.objects.filter(username=admin_username).exists():
            # Create the admin user
            User.objects.create_superuser(
                username=admin_username,
                email=admin_email,
                password=admin_password
            )
            self.stdout.write(self.style.SUCCESS(f"Admin user '{admin_username}' created successfully!"))
        else:
            self.stdout.write(self.style.SUCCESS(f"Admin user '{admin_username}' already exists."))

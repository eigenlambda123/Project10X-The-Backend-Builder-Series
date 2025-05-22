from django.contrib.auth import get_user_model
from djagno.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Create a superuser with the specified username and password'

    def handle(self, *args, **kwargs):
        """
        Handle the command to create a superuser.
        """
        User = get_user_model()
        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser(
                username='kiyo',
                email='admin@example.com',
                password='adminpass123'
            )
            self.stdout.write(self.style.SUCCESS('Superuser created.'))
        else:
            self.stdout.write(self.style.WARNING('Superuser already exists.'))
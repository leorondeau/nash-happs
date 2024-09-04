from django.core.management.base import BaseCommand
from nashhappsapi.views.bobbys_ig_azure import fetch_and_validate_instagram_posts  # Adjust the import path as needed

class Command(BaseCommand):
    help = 'Fetch Instagram posts'

    def handle(self, *args, **kwargs):
        fetch_and_validate_instagram_posts()
        self.stdout.write(self.style.SUCCESS('Successfully fetched Instagram posts'))

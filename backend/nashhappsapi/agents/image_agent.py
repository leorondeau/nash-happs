
from nashhappsapi.models import Event, Band, Venue, Creator
from tools.image_processor import extract_text_from_image
from datetime import datetime
import re
import sys
import os


def process_events(posts):
    for post in posts:
        has_date, extracted_text = extract_text_from_image(post)
        if has_date:
            save_event_details(post, extracted_text)
            break# Stop after finding the post with the current date
def save_event_details(post, extracted_text):
    band_names = re.findall(r'\b[A-Z][a-z]+\b', extracted_text)
    band_name = ' '.join(band_names) if band_names else'Unknown Band'

    venue, created = Venue.objects.get_or_create(
        name='Bobbys Idle Hour',
        defaults={'website': 'http://www.bobbysidlehour.com'}
    )

    band, created = Band.objects.get_or_create(name=band_name)

    creator, created = Creator.objects.get_or_create(
        username='admin',
        defaults={'email': 'admin@example.com', 'user_id': 1}
    )

    Event.objects.create(
        date=datetime.now().date(),
        venue=venue,
        band=band,
        time=datetime.now().time(),
        creator=creator
    )

    print(f"Post from {post.date} with shortcode {post.shortcode} saved to the database.")

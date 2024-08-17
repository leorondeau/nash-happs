from tools.ig_scraper import download_images
from tools.image_processor import extract_text_from_image
from nashhappsapi.models import Event, Band, Venue
from datetime import datetime

def process_events():
    # Define constants
    PROFILE_NAME = 'your_instagram_profile'
    VENUE_NAME = 'Bobbys Idle Hour'# Download images
    images = download_images(PROFILE_NAME)
    
    # Get or create venue
    venue, _ = Venue.objects.get_or_create(name=VENUE_NAME)
    
    # Delete previous day's events
    today = datetime.today().date()
    Event.objects.exclude(date=today).delete()
    
    for image_url in images:
        text = extract_text_from_image(image_url)
        # Process the text to extract dates, bands, and other details# Assuming you have a function to parse this text
        events = parse_event_text(text)
        
        for event in events:
            band, _ = Band.objects.get_or_create(name=event['band_name'])
            Event.objects.create(
                date=today,
                venue=venue,
                band=band,
                time=event['time'],
                creator=None# Assuming creator is not handled here
            )

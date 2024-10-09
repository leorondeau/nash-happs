import sys
import os

sys.path.append("/Users/admin/workspace/nash-happs/backend")

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nashhapps.settings')

# Now import and setup Django
import django
django.setup()


import glob
from instaloader import Instaloader, Profile
from azure_api_test import extract_text_from_image, is_current_week  # Import both functions
from django.db import transaction
from datetime import datetime
from nashhappsapi.models import Venue, Band, Event, Creator  # Adjust the import path as needed
from dotenv import load_dotenv

load_dotenv()
# Ensure temp directory exists
os.makedirs('temp', exist_ok=True)

# Function to fetch and validate Instagram posts

def fetch_and_validate_instagram_posts(username):
    L = Instaloader()
    profile = Profile.from_username(L.context, username)

    # Ensure the venue "Bobby's Idle Hour" exists
    venue, created = Venue.objects.get_or_create(
        name="Bobby's Idle Hour",
        defaults={'website': 'https://bobbysidlehour.com'}  # Add the website URL if needed
    )

    for post in profile.get_posts():
        print(f"Processing post: {post.shortcode}")

        # Download the post
        L.download_post(post, target='temp')

        # Find the downloaded image file
        image_files = glob.glob(f'temp/{post.date_utc.strftime("%Y-%m-%d_%H-%M-%S")}_UTC*.jpg')

        if not image_files:
            print(f"No image found for post {post.shortcode}.")
            continue

        image_path = image_files[0]

        # Extract text from image using the Azure function
        extracted_text_lines = extract_text_from_image(image_path)
        print(extracted_text_lines)
        # Validate if the post has the correct date range using the list of lines
        if is_current_week(extracted_text_lines):
            print(f"Post {post.shortcode} contains the correct date range.")
            
            # Extract event information (date, time, band name)
            save_event_to_db(extracted_text_lines, venue)
            
            # Stop processing further posts as the correct one is found
            break
        else:
            print(f"Post {post.shortcode} does not contain the correct date range. Deleting...")
            os.remove(image_path)

        # Clean up temp directory after processing
        for file in glob.glob("temp/*"):
            os.remove(file)

# Function to save event information to the database
@transaction.atomic
def save_event_to_db(extracted_text_lines, venue):
    # Example of parsing date, time, and band name from the extracted lines
    for line in extracted_text_lines:
        # Here you will need to parse the line to extract the band name, date, and time
        # This parsing logic needs to be specific to the format of the text in the images
        # For now, assume the format is 'BandName at 7:00 PM on August 30'
        # You can use regex or string splitting to extract this information

        # Example pseudo parsing (replace with actual parsing logic):
        if "pm" in line.lower() or "am" in line.lower():
            parts = line.split(" at ")
            if len(parts) == 2:
                band_name, time_str = parts[0], parts[1]

                # Parse time
                try:
                    event_time = datetime.strptime(time_str.strip(), "%I:%M %p").time()
                except ValueError:
                    print(f"Error parsing time: {time_str}")
                    continue

                # Create or get the band
                band, _ = Band.objects.get_or_create(name=band_name.strip())

                # Assume the date is today's date for simplicity (adjust as needed)
                event_date = datetime.now().date()

                # Create the event
                Event.objects.create(
                    date=event_date,
                    time=event_time,
                    band=band,
                    venue=venue
                )
                print(f"Saved event for band: {band_name} on {event_date} at {event_time}")

username="bobbysidlehourtavern"
fetch_and_validate_instagram_posts(username)
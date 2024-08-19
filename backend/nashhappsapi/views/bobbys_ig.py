import instaloader
import pytesseract
from PIL import Image
from datetime import datetime, timedelta
import re
import os
import glob
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nashhapps.settings')
django.setup()

from nashhappsapi.models import Venue, Band, Event

# Ensure temp directory exists
os.makedirs('temp', exist_ok=True)

# Regex pattern to identify date language (e.g., days of the week, times)
date_language_pattern = re.compile(
    r'\b(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday|AM|PM|am|pm|o\'clock)\b', re.IGNORECASE)

def fetch_bobbys_events():
    # Step 1: Download Instagram posts
    L = instaloader.Instaloader()
    username = 'bobbysidlehourtavern'
    profile = instaloader.Profile.from_username(L.context, username)

    # Function to extract text from image and check for date language
    def has_date_language(post):
        try:
            # Download the post
            L.download_post(post, target='temp')
            # Find the downloaded image file
            image_files = glob.glob(
                f'temp/{post.date_utc.strftime("%Y-%m-%d_%H-%M-%S")}_UTC*.jpg')

            if image_files:
                print(f"Found image file: {image_files[0]}")
                image_path = image_files[0]
                image = Image.open(image_path)
                text = pytesseract.image_to_string(image)
                return date_language_pattern.search(text), text
            else:
                print(f"Image for post {post.shortcode} was not found.")
            return False, ""
        except Exception as e:
            print(f"Error processing post {post.shortcode}: {e}")
            return False, ""
        # Iterate through posts
    today = datetime.now().date()
    venue, created = Venue.objects.get_or_create(name="Bobby's Idle Hour")
    
    for post in profile.get_posts():
        print(f"Processing post: {post.shortcode}")
        has_date, text = has_date_language(post)
        if has_date:
            print("Date language found")
            
            # Extract the date range
            date_range_pattern = re.compile(r'(\w+ \d+-\d+)')
            date_range_match = date_range_pattern.search(text)
            
            if not date_range_match:
                date_range_pattern = re.compile(r'(\w+)(\d+)-(\d+)', re.IGNORECASE)
                date_range_match = date_range_pattern.search(text)

            
            if date_range_match:
                if ' ' in date_range_match.group(1):
                    start_month_day, end_day = date_range_match.group(1).split('-')
                else:
                    start_month = date_range_match.group(1)[:3]
                    start_day = date_range_match.group(1)[3:]
                    end_day = date_range_match.group(2)
                    start_month_day = f"{start_month}{start_day}"
                    
                start_month, start_day = start_month_day.split()
                start_day = int(start_day)
                end_day = int(end_day)

                # Convert the date range to actual dates
                start_date = datetime.strptime(f"{start_month}{start_day}{datetime.now().year}", "%b %d %Y")
                days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
                day_to_date = {days_of_week[i]: (start_date + timedelta(days=i)).strftime("%A, %B %d") for i in range(len(days_of_week))}

                # Extract and save today's events
                day_event_pattern = re.compile(r'(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)\s*(.*?)\s*(?=(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday|$))', re.DOTALL)
                found_today = False 
                for day_event in day_event_pattern.findall(text):
                    day, events, _ = day_event
                    event_date_str = day_to_date.get(day.strip())

                    if event_date_str:
                        event_date = datetime.strptime(event_date_str, '%A, %B %d').date()

                        if event_date == today:
                            found_today = True
                            for event in events.strip().split('\n'):
                                band_name = event.strip()
                                band, created = Band.objects.get_or_create(name=band_name)
                                Event.objects.create(
                                    date=event_date,
                                    venue=venue,
                                    band=band,
                                    time=datetime.now().time()  # Assuming time is not provided, use current time
                                )
                                print(f"Saved event: {event_date}, {band_name}")
                            break
                        # Stop processing further as today's date is found
                        if found_today:
                            print("Today's events found and saved.")
                            break
                        # Stop processing further posts 
if __name__ == "__main__":
    fetch_bobbys_events()
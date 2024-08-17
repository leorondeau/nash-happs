from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.apps import apps
import requests
from bs4 import BeautifulSoup
from datetime import datetime

class TheLocalEventViewSet(viewsets.ViewSet):
    
    @action(detail=False, methods=['get'])
    def fetch_local_events(self, request):
        # Ensure models are imported after the app registry is ready
        Event = apps.get_model('nashhappsapi', 'Event')
        Venue = apps.get_model('nashhappsapi', 'Venue')
        Band = apps.get_model('nashhappsapi', 'Band')

        url = 'https://localnash.com/calendar/'
        today = datetime.today().date()
        
        # Delete existing events that are not today's date
        Event.objects.exclude(date=today).delete()

        venue, created = Venue.objects.get_or_create(
            name='The Local',
            defaults={'website': 'http://www.localnash.com'}
        )

        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            calendar_events = soup.find_all('div', attrs={'data-mec-cell': today.strftime('%Y%m%d')})

            for local_event in calendar_events:
                event_titles = local_event.find_all('h4', class_='mec-event-title')
                
                for title_tag in event_titles:
                    event_title = title_tag.text.strip() if title_tag else'No title found'
                    local_band, created = Band.objects.get_or_create(name=event_title)
                    
                    time_tag = local_event.find('div', class_='mec-event-time mec-color')
                    event_time_str = time_tag.text.strip() if time_tag else'00:00 AM'
                    try:
                        event_time = datetime.strptime(event_time_str, '%I:%M %p').time()
                    except ValueError:
                        print(f"Error parsing time: {event_time_str}")
                        event_time = datetime.strptime('00:00 AM', '%I:%M %p').time()
                    
                    # Save the event to the database
                    Event.objects.create(
                        date=today,
                        venue=venue,
                        band=local_band,
                        time=event_time,
                        creator=None# Set creator to None or the appropriate creator instance
                    )
            return Response(status=status.HTTP_200_OK)
        else:
            return Response({"error": "Failed to fetch webpage"}, status=status.HTTP_400_BAD_REQUEST)

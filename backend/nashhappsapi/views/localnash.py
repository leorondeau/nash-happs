from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from nashhappsapi.models import Event, Venue, Band, Creator
from rest_framework import serializers
import requests
from bs4 import BeautifulSoup
from datetime import datetime

class BandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Band
        fields = '__all__'

class CreatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Creator
        fields = '__all__'

class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

class TheLocalEventViewSet(viewsets.ViewSet):
    
    @action(detail=False, methods=['get'])
    def fetch_events(self, request):
        url = 'https://localnash.com/calendar/'
        today = datetime.today().strftime('%Y%m%d')
        venue, created = Venue.objects.get_or_create(
            name='The Local',
            defaults={'website': 'http://www.localnash.com'}
        )

        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            calendar_events = soup.find_all('div', attrs={'data-mec-cell': today})

            events = []
            for local_event in calendar_events:
                event_titles = local_event.find_all('h4', class_='mec-event-title')
                
                for title_tag in event_titles:
                    event_title = title_tag.text.strip() if title_tag else 'No title found'
                    local_band, created = Band.objects.get_or_create(name=event_title)
                    
                    time_tag = local_event.find('div', class_='mec-event-time mec-color')
                    event_time_str = time_tag.text.strip() if time_tag else '00:00 AM'
                    
                    try:
                        event_time = datetime.strptime(event_time_str, '%I:%M %p').time()
                    except ValueError:
                        print(f"Error parsing time: {event_time_str}")
                        event_time = datetime.strptime('00:00 AM', '%I:%M %p').time()
                    
                    event_data = {
                        'date': datetime.today().date(),
                        'venue': venue.id,
                        'band': local_band.id,
                        'time': event_time,
                        'creator': None  # or the appropriate creator ID
                    }
                    
                    serializer = EventSerializer(data=event_data)
                    if serializer.is_valid():
                        event = serializer.save()
                        events.append(serializer.data)
                    else:
                        print(f"Serializer errors: {serializer.errors}")
            
            return Response(events, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Failed to fetch webpage"}, status=status.HTTP_400_BAD_REQUEST)

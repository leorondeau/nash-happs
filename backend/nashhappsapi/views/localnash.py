from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from nashhappsapi.models import Event, Venue, Band, Creator
from rest_framework import serializers
import requests
from bs4 import BeautifulSoup
from datetime import datetime

class TheLocalEventViewSet(viewsets.ViewSet):
    
    @action(detail=False, methods=['get'])
    def fetch_events(self, request):
        
        
        url = 'https://localnash.com/calendar/'
        today = datetime.today().strftime('%Y%m%d')

        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            calendar_events = soup.find_all('div', attrs={'data-mec-cell': today})

            events = []
            for event in calendar_events:
                event_titles = event.find_all('h4', class_='mec-event-title')
                for title_tag in event_titles:
                    event_title = title_tag.text.strip() if title_tag else 'No title found'
                    # event_time = event.find('span', class_='mec-event-time').text.strip()  # Adjust selector

                    events.append({
                        'date': today,
                        'title': event_title,
                        # 'time': event_time,
                        'description': "Lipsum"
                    })
            
            # venue = Venue.objects.get(name='The Local')
            # Assuming band names are matched to event titles, adjust as necessary
            for event in events:
                event_date = datetime.strptime(event['date'], '%Y%m%d').date()
                # event_time = datetime.strptime(event['time'], '%I:%M %p').time()  # Adjust time format if necessary

                event_data = {
                    'date': event_date,
                    # 'venue': venue.id,
                    'band': Band.objects.get_or_create(name=event['title'])[0].id,
                    # 'time': event_time,
                    # 'creator': creator.id  # Add as needed
                }

                serializer = EventSerializer(data=event_data)
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            return Response(events, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Failed to fetch webpage"}, status=status.HTTP_400_BAD_REQUEST)


class BandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Band
        fields = '__all__'

class CreatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Creator
        fields = '__all__'

# class VenueSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Venue
#         fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

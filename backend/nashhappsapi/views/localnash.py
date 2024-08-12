import requests
from bs4 import BeautifulSoup
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from models import Event, Venue, Band, Creator


class TheLocalEventView(APIView):

    def get(self, request):
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
                    event_time = event.find('span', class_='mec-event-time').text.strip()  # Adjust selector

                    events.append({
                        'date': today,
                        'title': event_title,
                        'time': event_time,
                        'description': "Lipsum"
                    })
            
            # Example: Assume venue_name, band_name, creator_username are provided in the request
            venue_name = request.GET.get('venue_name', 'Default Venue')
            band_name = request.GET.get('band_name', 'Default Band')
            creator_username = request.GET.get('creator_username', 'Default Creator')

            venue = Venue.objects.get(name=venue_name)
            band = Band.objects.get(name=band_name)
            creator = Creator.objects.get(username=creator_username)
            
            for event in events:
                event_date = datetime.strptime(event['date'], '%Y%m%d').date()
                event_time = datetime.strptime(event['time'], '%I:%M %p').time()  # Adjust time format if necessary

                event_data = {
                    'date': event_date,
                    'venue': venue.id,
                    'band': band.id,
                    'time': event_time,
                    'creator': creator.id
                }

                serializer = EventSerializer(data=event_data)
                if serializer.is_valid():
                    serializer.save()
                else:
                    print(serializer.errors)
            
            return Response(events, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Failed to fetch webpage"}, status=status.HTTP_400_BAD_REQUEST)


class BandSerializer(ModelSerializer):
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
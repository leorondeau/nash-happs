from rest_framework import viewsets, serializers
from rest_framework.response import Response
from nashhappsapi.models import Event


class FetchEventsViewSet(viewsets.ViewSet):
    # Serializer defined within the ViewSet
    class EventSerializer(serializers.ModelSerializer):
        class Meta:
            model = Event
            fields = '__all__'

    def list(self, request):
        # Retrieve all events from the database
        events = Event.objects.all()
        # Serialize the events data
        serializer = self.EventSerializer(events, many=True)
        # Return the serialized data as JSON response
        return Response(serializer.data)
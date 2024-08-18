from rest_framework import viewsets
from rest_framework.response import Response
from agents.image_agent import process_instagram_events

class BobbyIGViewSet(viewsets.ViewSet):

    def list(self, request):
        ig_account = 'bobbysidlehourtavern'# Instagram account to scrape
        process_instagram_events(ig_account)
        return Response({"status": "Events processed"})

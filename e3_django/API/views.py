from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from .serializers import UploadSerializer
import json

from django.http import HttpResponse

class UploadViewSet(ViewSet):
    serializer_class = UploadSerializer

    def list(self, request):
        """
        Purpose: Sends a GET request to view main homepage.
        """
        return Response("GET API")


    def create(self, request):
        """
        Purpose: Sends a POST request to upload user's input JSON file.
        """
        file_uploaded = request.FILES.get('file_uploaded')
        content_type = file_uploaded.content_type
        response = "POST API and you have uploaded a {} file".format(content_type)
        return Response(response)


    def download(self, request):
        """
        Purpose: Sends a request to send data to user in downloadable form.
        """
        return Response('File downloaded')
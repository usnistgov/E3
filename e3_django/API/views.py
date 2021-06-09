from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.viewsets import ViewSet

from API.serializers import InputSerializer


class AnalysisViewSet(ViewSet):
    """
    Resource to begin analysis.
    """
    def create(self, request):
        serializer = InputSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

        print(serializer.validated_data)

        return Response(status=HTTP_202_ACCEPTED, headers={"Location": f"{request.path}queue/"})


class QueueViewSet(ViewSet):
    """
    Resource to query condition of analysis job
    """
    def list(self, request):
        return Response("Hello World")
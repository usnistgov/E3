from celery.result import AsyncResult
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.viewsets import ViewSet, ModelViewSet

from API import tasks
from API.serializers import InputSerializer

import logging

logger = logging.getLogger(__name__)


class AnalysisViewSet(ViewSet):
    """
    Resource to begin analysis.
    """
    def create(self, request):
        serializer = InputSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

        task = tasks.analyze.delay(serializer.validated_data)

        return Response(status=HTTP_202_ACCEPTED, headers={
            "Location": request.build_absolute_uri(f"/api/v1/queue/{task.task_id}")
        })


class QueueViewSet(ViewSet):
    """
    Resource to query condition of analysis job
    """
    def retrieve(self, request, pk=None):
        if pk is None:
            return Response("ID must be specified", status=HTTP_400_BAD_REQUEST)

        status = AsyncResult(pk).status

        if status == "SUCCESS":
            return Response(status=HTTP_303_SEE_OTHER, headers={
                "Location": request.build_absolute_uri(f"/api/v1/result/{pk}")
            })
        else:
            return Response(status)


class ResultViewSet(ViewSet):
    """
    Resource to get the result of an analysis job
    """
    def retrieve(self, request, pk=None):
        if pk is None:
            return Response("ID must be specified", status=HTTP_400_BAD_REQUEST)

        result = AsyncResult(pk)

        if result.ready():
            return Response(result.get())
        else:
            return Response(status=HTTP_404_NOT_FOUND)

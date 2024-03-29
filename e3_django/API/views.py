import logging

from celery.result import AsyncResult
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.viewsets import ViewSet
from rest_framework_api_key.permissions import HasAPIKey

from API import tasks
from API.serializers.InputSerializer import InputSerializer
from frontend.models import UserAPIKey


class HeaderApiKey(HasAPIKey):
    model = UserAPIKey


class AnalysisViewSet(ViewSet):
    """
    Resource to begin analysis.
    """
    permission_classes = [HeaderApiKey]

    def create(self, request):
        logging.debug(f"Analysis View called with request data:\n{request.data}\n")

        serializer = InputSerializer(data=request.data)

        if not serializer.is_valid():
            logging.debug(f"Failed to validate data! Data was:\n{request.data}\n")
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

        task = tasks.analyze.delay(serializer.save())

        logging.debug(f"\nAnalysis finished\n")

        return Response(task.get())

        # return Response(status=HTTP_202_ACCEPTED, headers={
        #     "Location": request.build_absolute_uri(f"/api/v1/queue/{task.task_id}")
        # })


class QueueViewSet(ViewSet):
    """
    Resource to query condition of analysis job
    """
    permission_classes = [HeaderApiKey]

    def retrieve(self, request, pk=None):
        if pk is None:
            return Response("ID must be specified", status=HTTP_400_BAD_REQUEST)

        status = AsyncResult(pk).status

        logging.debug(f"Status of task {pk} is {status}")

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
    permission_classes = [HeaderApiKey]

    def retrieve(self, request, pk=None):
        if pk is None:
            return Response("ID must be specified", status=HTTP_400_BAD_REQUEST)

        result = AsyncResult(pk)

        if result.ready():
            return Response(result.get())
        else:
            return Response(status=HTTP_404_NOT_FOUND)

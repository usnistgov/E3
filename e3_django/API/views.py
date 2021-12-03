import logging

import rx
import rx.operators
from celery.result import AsyncResult
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.viewsets import ViewSet
from rest_framework_api_key.permissions import HasAPIKey

from API import tasks
from API.serializers.InputSerializer import InputSerializer
from frontend.models import UserAPIKey


class UrlOrHeaderApiKey(HasAPIKey):
    """
    Permissions that checks if API key is present in the default HTTP header or a URL parameter.
    """
    model = UserAPIKey

    def get_key(self, request):
        """
        Returns the API key if it is present in an HTTP header else it tries to get it from a URL parameter. If no key
        is found, None will be returned.

        :param request: The HTTP request to get the key from.
        :return: The API key or None if no key is present.
        """
        header_key = super().get_key(request)
        return header_key if header_key else request.GET.get("key")


@api_view(['POST'])
@permission_classes([UrlOrHeaderApiKey])
def analyze(request):
    request_stream = rx.of(request)
    request_stream.pipe(
        rx.operators.map(lambda r: r.data)
    )

    #logging.debug(f"POST called on analysis resource with request data: \n{request.data}\n")

    #serializer = InputSerializer(data=request.data)

    #if not serializer.is_valid():
    #    logging.debug(f"Failed to validate data! Data was:\n{request.data}\n")
    #    return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    #task = tasks.analyze.delay(serializer.save())

    #logging.debug(f"\nAnalysis finished\n")

    #return Response(task.get())

    # return Response(status=HTTP_202_ACCEPTED, headers={
    #     "Location": request.build_absolute_uri(f"/api/v1/queue/{task.task_id}")
    # })


@api_view
@permission_classes([UrlOrHeaderApiKey])
def queue(request, pk=None):
    """
    The queue resource queries if the given task is finished or not. If the task is finished, a redirect to the
    completed resource will be returned.

    :param request: The request object
    :param pk: The ID of the task
    :return: A redirect to the task result
    """
    logging.debug(f"Queue resource called with parameter {pk}")

    try:
        status = AsyncResult(pk).status

        if status == "SUCCESS":
            logging.debug(f"Task with ID {pk} is completed, returning redirect")
            return Response(status=HTTP_303_SEE_OTHER, headers={
                "Location": request.build_absolute_uri(f"/api/v1/result/{pk}")
            })

        logging.debug(f"Task with ID {pk} is not complete. Status: {status}")
        return Response(status)
    except ValueError:
        logging.debug(f"Task ID {pk} not found")
        return Response("ID must be specified", status=HTTP_400_BAD_REQUEST)


@api_view
@permission_classes([UrlOrHeaderApiKey])
def result(_, pk=None):
    """
    The result resource gets the task with the given ID and returns its result.

    :param _: Request is ignored
    :param pk: The ID of the task
    :return: The result of the task
    """
    logging.debug(f"Result resource called with parameter {pk}")

    try:
        async_result = AsyncResult(pk)

        if async_result.ready():
            logging.debug(f"Result resource returning result for task {pk}")
            return Response(async_result.get())

        logging.debug(f"Task with ID {pk} is not ready")
        return Response(status=HTTP_404_NOT_FOUND)
    except ValueError:
        logging.debug(f"Result resource failed to find task with ID {pk}")
        return Response("ID must be specified", status=HTTP_400_BAD_REQUEST)

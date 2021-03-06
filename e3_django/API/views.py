import logging
from decimal import Decimal
from functools import reduce
from operator import add

from celery.result import AsyncResult
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.viewsets import ViewSet
from rest_framework_api_key.permissions import HasAPIKey

from API import tasks
from API.serializers import InputSerializer, BCN, OutputSerializer, \
    CashFlowSerializer

logger = logging.getLogger(__name__)


class UrlOrHeaderApiKey(HasAPIKey):
    def get_key(self, request):
        header_key = super().get_key(request)
        return header_key if header_key else request.GET.get("key")


class AnalysisViewSet(ViewSet):
    """
    Resource to begin analysis.
    """
    permission_classes = [UrlOrHeaderApiKey]

    def create(self, request):
        serializer = InputSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

        bcns = [BCN(25, **args) for args in serializer.validated_data["bcnObjects"]]

        for bcn in bcns:
            logger.info(bcn)
            logger.info(bcn.discount(Decimal(0.06)))

        for alt in serializer.validated_data["alternativeObjects"]:
            flows = map(lambda x: x.discount(Decimal(0.06)), filter(lambda x: x.bcnID in alt["altBCNList"], bcns))
            logger.info(list(reduce(lambda x, y: map(add, x, y), flows)))

        #logger.info(serializer.validated_data["alternativeObjects"])

        #for alt in serializer.validated_data["alternativeObjects"]:
        #    logger.info(Alternative(alt).altID)


        task = tasks.analyze.delay(serializer.validated_data)

        # output = OutputSerializer(CashFlowSerializer())

        # logger.log(output.data)

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

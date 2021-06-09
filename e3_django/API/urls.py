from django.urls import path, include
from rest_framework import routers

from API.views import AnalysisViewSet, QueueViewSet

router = routers.DefaultRouter()
router.register(r'analysis', AnalysisViewSet, basename="analysis")
router.register(r'queue', QueueViewSet, basename="queue")

urlpatterns = [
    # Wire up the API using automatic URL routing
    path('', include(router.urls))
]

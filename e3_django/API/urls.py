from django.urls import path, include
from rest_framework import routers

from API.views import QueueViewSet, ResultViewSet, analyze

router = routers.DefaultRouter()
router.register(r'queue', QueueViewSet, basename="queue")
router.register(r'result', ResultViewSet, basename="result")

urlpatterns = [
    # Wire up the API using automatic URL routing
    path('', include(router.urls)),
    path('analysis', analyze)
]

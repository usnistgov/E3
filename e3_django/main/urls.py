from django.urls import path, include
from rest_framework import routers
from .views import UploadViewSet

router = routers.DefaultRouter()
router.register(r'upload', UploadViewSet, basename="upload")


from . import views

urlpatterns = [
    # Wire up the API using automatic URL routing
    path('', include(router.urls))
    #path('', views.index, name='index'),
]
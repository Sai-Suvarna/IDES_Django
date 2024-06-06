from django.contrib import admin
from django.urls import path, include

from rest_framework.routers import DefaultRouter
from core.views import RequestDetailsView

router = DefaultRouter()
router.register(r'request-details', RequestDetailsView, basename='requestdetails')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('core.urls')),  # Include app URLs from core
    path('api/', include(router.urls)),  # Include the router's URLs
]


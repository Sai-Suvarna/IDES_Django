from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
# from core.views import WebcamImageUploadView



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('core.urls')),  # Include app URLs from core
    # path('api/upload/', WebcamImageUploadView.as_view(), name='webcam-image-upload'),
    # path('', RedirectView.as_view(url='/api/process-word/', permanent=True)),  # Redirect root to API
]

from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('core.urls')),  # Include app URLs from core
    # path('', RedirectView.as_view(url='/api/process-word/', permanent=True)),  # Redirect root to API
]

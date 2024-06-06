from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views import ProcessWordView, UploadImageView, WebcamImageUploadView, get_product_details, ProductDetailsList, RequestDetailsView
from core.views import RequestDetailsListView


urlpatterns = [
    path('process-word/', ProcessWordView.as_view(), name='process-word'),
    path('upload_image/', UploadImageView.as_view(), name='upload_image'),
    path('upload/', WebcamImageUploadView.as_view(), name='webcam-image-upload'),
    path('product-details/<str:input_word>/', get_product_details, name='get_product_details'),
    path('productdetails/', ProductDetailsList.as_view(), name='productdetails-list'),
    path('request-details-list/', RequestDetailsListView.as_view(), name='request-details-list'),

]




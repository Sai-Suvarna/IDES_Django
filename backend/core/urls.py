from django.urls import path
from core.views import ProcessWordView
from core.views import UploadImageView
from core.views import WebcamImageUploadView
from core.views import get_product_details
from core.views import ProductDetailsList



urlpatterns = [
    path('process-word/', ProcessWordView.as_view(), name='process-word'),
    path('upload_image/', UploadImageView.as_view(), name='upload_image'),
    path('upload/', WebcamImageUploadView.as_view(), name='webcam-image-upload'),
    path('product-details/<str:input_word>/', get_product_details, name='get_product_details'),
    path('productdetails/', ProductDetailsList.as_view(), name='productdetails-list'),

]

from django.urls import path
from .views import BrandListAPIView, BrandCreateAPIView, MobileListAPIView, MobileCreateAPIView, SearchAPIView

urlpatterns = [
    path('brands/', BrandListAPIView.as_view(), name='brand_list_api'),
    path('brands/new/', BrandCreateAPIView.as_view(), name='brand_create_api'),
    path('mobiles/', MobileListAPIView.as_view(), name='mobile_list_api'),
    path('mobiles/new/', MobileCreateAPIView.as_view(), name='mobile_create_api'),
    path('search/', SearchAPIView.as_view(), name='search_api'),
]

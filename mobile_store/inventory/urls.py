from django.urls import path
from .views import BrandListView, BrandCreateView, MobileListView, MobileCreateView, SearchView

urlpatterns = [
    path('brands/', BrandListView.as_view(), name='brand_list'),
    path('brands/new/', BrandCreateView.as_view(), name='brand_create'),
    path('mobiles/', MobileListView.as_view(), name='mobile_list'),
    path('mobiles/new/', MobileCreateView.as_view(), name='mobile_create'),
    path('search/', SearchView.as_view(), name='search_view'),

]

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404, redirect
from ...models import Brand, Mobile
from ...forms import BrandForm, MobileForm


class BrandListAPIView(APIView):
    def get(self, request):
        brands = Brand.objects.all().values('name', 'nationality')
        return Response(brands)


class BrandCreateAPIView(APIView):
    def get(self, request):
        form = BrandForm()
        return Response({'form': form.as_p()})

    def post(self, request):
        form = BrandForm(request.data)
        if form.is_valid():
            form.save()
            return Response({'message': 'Brand created successfully'}, status=status.HTTP_201_CREATED)
        return Response({'errors': form.errors}, status=status.HTTP_400_BAD_REQUEST)


class MobileListAPIView(APIView):
    def get(self, request):
        mobiles = Mobile.objects.all().values('brand__name', 'model', 'price', 'color', 'screen_size', 'status',
                                              'manufacturer_country')
        return Response(mobiles)


class MobileCreateAPIView(APIView):
    def get(self, request):
        form = MobileForm()
        return Response({'form': form.as_p()})

    def post(self, request):
        form = MobileForm(request.data)
        if form.is_valid():
            form.save()
            return Response({'message': 'Mobile created successfully'}, status=status.HTTP_201_CREATED)
        return Response({'errors': form.errors}, status=status.HTTP_400_BAD_REQUEST)


class SearchAPIView(APIView):
    def get(self, request):
        query_type = request.GET.get('query_type')
        if not query_type:
            return Response({'error': 'query_type parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

        if query_type == 'korea_brands':
            return self.korea_brands()
        elif query_type == 'brand_mobiles':
            brand_name = request.GET.get('brand_name')
            return self.brand_mobiles(brand_name)
        elif query_type == 'nationality_match':
            return self.nationality_match()
        else:
            return Response({"error": "Invalid query type"}, status=status.HTTP_400_BAD_REQUEST)

    def korea_brands(self):
        brands = Brand.objects.filter(nationality='Korea').values('name')
        return Response(brands)

    def brand_mobiles(self, brand_name):
        if not brand_name:
            return Response({"error": "brand_name parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
        mobiles = Mobile.objects.filter(brand__name=brand_name).values('model', 'price', 'color', 'screen_size',
                                                                       'status', 'manufacturer_country')
        return Response(mobiles)

    def nationality_match(self):
        mobiles = Mobile.objects.filter(brand__nationality=F('manufacturer_country')).values('brand__name', 'model',
                                                                                             'price', 'color',
                                                                                             'screen_size', 'status',
                                                                                             'manufacturer_country')
        return Response(mobiles)

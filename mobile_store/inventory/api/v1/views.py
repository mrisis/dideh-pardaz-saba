from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ...models import Brand, Mobile
from .serializers import BrandSerializer, MobileSerializer
from django.db.models import F


class BrandListAPIView(APIView):
    def get(self, request):
        brands = Brand.objects.all()
        serializer = BrandSerializer(brands, many=True)
        return Response(serializer.data)


class BrandCreateAPIView(APIView):
    def post(self, request):
        serializer = BrandSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Brand created successfully'}, status=status.HTTP_201_CREATED)
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class MobileListAPIView(APIView):
    def get(self, request):
        mobiles = Mobile.objects.all()
        serializer = MobileSerializer(mobiles, many=True)
        return Response(serializer.data)


class MobileCreateAPIView(APIView):
    def post(self, request):
        serializer = MobileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Mobile created successfully'}, status=status.HTTP_201_CREATED)
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


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
        brands = Brand.objects.filter(nationality='Korea')
        serializer = BrandSerializer(brands, many=True)
        return Response(serializer.data)

    def brand_mobiles(self, brand_name):
        if not brand_name:
            return Response({"error": "brand_name parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
        mobiles = Mobile.objects.filter(brand__name=brand_name)
        serializer = MobileSerializer(mobiles, many=True)
        return Response(serializer.data)

    def nationality_match(self):
        mobiles = Mobile.objects.filter(brand__nationality=F('manufacturer_country'))
        serializer = MobileSerializer(mobiles, many=True)
        return Response(serializer.data)

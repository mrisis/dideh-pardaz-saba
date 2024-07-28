from django.shortcuts import render, redirect
from django.views import View
from .models import Brand, Mobile
from .forms import BrandForm, MobileForm
from django.http import JsonResponse
from django.db.models import F


class BrandListView(View):
    def get(self, request):
        brands = Brand.objects.all()
        return render(request, 'inventory/brand_list.html', {'brands': brands})


class BrandCreateView(View):
    def get(self, request):
        form = BrandForm()
        return render(request, 'inventory/brand_form.html', {'form': form})

    def post(self, request):
        form = BrandForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('brand_list')
        return render(request, 'inventory/brand_form.html', {'form': form})


class MobileListView(View):
    def get(self, request):
        mobiles = Mobile.objects.all()
        return render(request, 'inventory/mobile_list.html', {'mobiles': mobiles})


class MobileCreateView(View):
    def get(self, request):
        form = MobileForm()
        return render(request, 'inventory/mobile_form.html', {'form': form})

    def post(self, request):
        form = MobileForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('mobile_list')
        return render(request, 'inventory/mobile_form.html', {'form': form})


class SearchView(View):
    def get(self, request):
        query_type = request.GET.get('query_type')
        if query_type is None:
            return render(request, 'inventory/search.html')

        if query_type == 'korea_brands':
            return self.korea_brands()
        elif query_type == 'brand_mobiles':
            brand_name = request.GET.get('brand_name')
            return self.brand_mobiles(brand_name)
        elif query_type == 'nationality_match':
            return self.nationality_match()
        else:
            return JsonResponse({"error": "Invalid query type"}, status=400)

    def korea_brands(self):
        brands = Brand.objects.filter(nationality='Korea').values('name')
        return JsonResponse(list(brands), safe=False)

    def brand_mobiles(self, brand_name):
        mobiles = Mobile.objects.filter(brand__name=brand_name).values('model', 'price', 'color', 'screen_size',
                                                                       'status', 'manufacturer_country')
        return JsonResponse(list(mobiles), safe=False)

    def nationality_match(self):
        mobiles = Mobile.objects.filter(brand__nationality=F('manufacturer_country')).values('brand__name',
                                                                                                    'model', 'price',
                                                                                                    'color',
                                                                                                    'screen_size',
                                                                                                    'status',
                                                                                                    'manufacturer_country')
        return JsonResponse(list(mobiles), safe=False)

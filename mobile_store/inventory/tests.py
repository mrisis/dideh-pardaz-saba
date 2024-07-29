from django.test import TestCase, Client
from django.urls import reverse
from .models import Brand, Mobile
from .forms import MobileForm, BrandForm
from django.db import IntegrityError


class BrandListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('brand_list')
        self.brand1 = Brand.objects.create(name="Brand1", nationality="Korea")
        self.brand2 = Brand.objects.create(name="Brand2", nationality="USA")

    def test_get_brands(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventory/brand_list.html')
        self.assertContains(response, self.brand1.name)
        self.assertContains(response, self.brand2.name)


class BrandCreateViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('brand_create')

    def test_get_brand_form(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventory/brand_form.html')
        self.assertIsInstance(response.context['form'], BrandForm)

    def test_post_valid_brand(self):
        data = {
            'name': 'Brand3',
            'nationality': 'Japan'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('brand_list'))
        self.assertTrue(Brand.objects.filter(name='Brand3').exists())

    def test_post_invalid_brand(self):
        data = {
            'name': '',
            'nationality': 'Japan'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventory/brand_form.html')
        self.assertFalse(Brand.objects.filter(nationality='Japan').exists())


class MobileListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('mobile_list')
        self.brand = Brand.objects.create(name="Brand1", nationality="Korea")
        self.mobile1 = Mobile.objects.create(brand=self.brand, model="Model1", price=100, color="Black", screen_size=5,
                                             status="-", manufacturer_country="Korea")
        self.mobile2 = Mobile.objects.create(brand=self.brand, model="Model2", price=200, color="White", screen_size=6,
                                             status="+", manufacturer_country="Korea")

    def test_get_mobiles(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventory/mobile_list.html')
        self.assertContains(response, self.mobile1.model)
        self.assertContains(response, self.mobile2.model)


class MobileCreateViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('mobile_create')
        self.brand = Brand.objects.create(name="Brand1", nationality="Korea")

    def test_get_mobile_form(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventory/mobile_form.html')
        self.assertIsInstance(response.context['form'], MobileForm)

    def test_post_valid_mobile(self):
        data = {
            'brand': self.brand.id,
            'model': 'Model3',
            'price': 300,
            'color': 'Blue',
            'screen_size': 7,
            'status': '+',
            'manufacturer_country': 'Korea'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('mobile_list'))
        self.assertTrue(Mobile.objects.filter(model='Model3').exists())

    def test_post_invalid_mobile(self):
        data = {
            'brand': self.brand.id,
            'model': '',
            'price': 300,
            'color': 'Blue',
            'screen_size': 7,
            'status': '+',
            'manufacturer_country': 'Korea'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventory/mobile_form.html')
        self.assertFalse(Mobile.objects.filter(price=300).exists())


class SearchViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('search_view')
        self.brand_korea = Brand.objects.create(name="BrandKorea", nationality="Korea")
        self.brand_usa = Brand.objects.create(name="BrandUSA", nationality="USA")
        self.mobile1 = Mobile.objects.create(brand=self.brand_korea, model="Model1", price=100, color="Black",
                                             screen_size=5, status="+", manufacturer_country="Korea")
        self.mobile2 = Mobile.objects.create(brand=self.brand_usa, model="Model2", price=200, color="White",
                                             screen_size=6, status="-", manufacturer_country="USA")

    def test_korea_brands(self):
        response = self.client.get(self.url, {'query_type': 'korea_brands'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'BrandKorea')
        self.assertNotContains(response, 'BrandUSA')

    def test_brand_mobiles(self):
        response = self.client.get(self.url, {'query_type': 'brand_mobiles', 'brand_name': 'BrandKorea'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Model1')
        self.assertNotContains(response, 'Model2')

    def test_nationality_match(self):
        response = self.client.get(self.url, {'query_type': 'nationality_match'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Model1')
        self.assertContains(response, 'Model2')

    def test_invalid_query_type(self):
        response = self.client.get(self.url, {'query_type': 'invalid_query'})
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {"error": "Invalid query type"})


class TestBrandModel(TestCase):
    def test_brand_creation(self):
        brand = Brand.objects.create(name="Test Brand", nationality="USA")
        self.assertEqual(brand.name, "Test Brand")
        self.assertEqual(brand.nationality, "USA")
        self.assertEqual(str(brand), "Test Brand")

    def test_brand_unique_name(self):
        Brand.objects.create(name="Unique Brand", nationality="UK")
        with self.assertRaises(IntegrityError):
            Brand.objects.create(name="Unique Brand", nationality="Germany")


class TestMobileModel(TestCase):
    def setUp(self):
        self.brand = Brand.objects.create(name="BrandX", nationality="Korea")

    def test_mobile_creation(self):
        mobile = Mobile.objects.create(
            brand=self.brand,
            model="ModelY",
            price=500,
            color="Black",
            screen_size=5,
            status='+',
            manufacturer_country="China"
        )
        self.assertEqual(mobile.brand, self.brand)
        self.assertEqual(mobile.model, "ModelY")
        self.assertEqual(str(mobile), "BrandX ModelY")

    def test_mobile_unique_model(self):
        Mobile.objects.create(
            brand=self.brand,
            model="UniqueModel",
            price=300,
            color="White",
            screen_size=6,
            status='-',
            manufacturer_country="USA"
        )
        with self.assertRaises(IntegrityError):
            Mobile.objects.create(
                brand=self.brand,
                model="UniqueModel",
                price=400,
                color="Blue",
                screen_size=7,
                status='+',
                manufacturer_country="UK"
            )

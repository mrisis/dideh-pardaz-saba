from django import forms
from .models import Brand, Mobile


class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['name', 'nationality']


class MobileForm(forms.ModelForm):
    class Meta:
        model = Mobile
        fields = ['brand', 'model', 'price', 'color', 'screen_size', 'status', 'manufacturer_country']

from django.contrib import admin
from .models import Brand, Mobile


class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'nationality')
    search_fields = ('name', 'nationality')
    ordering = ('name',)
    list_filter = ('nationality',)


class MobileAdmin(admin.ModelAdmin):
    list_display = ('brand', 'model', 'price', 'color', 'screen_size', 'status', 'manufacturer_country')
    search_fields = ('brand__name', 'model', 'color', 'manufacturer_country')
    list_filter = ('brand', 'status', 'manufacturer_country')
    ordering = ('brand', 'model')


admin.site.register(Brand, BrandAdmin)
admin.site.register(Mobile, MobileAdmin)

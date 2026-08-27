from django.contrib import admin

from apps.hotel.models import Hotel


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('id', 'partner', 'city_code', 'region_code', 'rating', 'created_at')
    list_filter = ('city_code', 'region_code')
    search_fields = ('partner__name', 'address')

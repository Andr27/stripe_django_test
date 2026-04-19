from django.contrib import admin
from .models import Item, Order, Discount, Tax



@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price', 'currency')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'get_total_price', 'discount', 'tax')
    filter_horizontal = ('items',)
    search_fields = ('id', 'discount__name', 'tax__name')
    list_filter = ('created_at', 'discount', 'tax')



@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('name', 'percent_off', 'stripe_coupon_id')


@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    list_display = ('name', 'percent', 'stripe_tax_rate_id')






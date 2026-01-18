from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product', 'price']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status', 'total_price', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['user__username', 'shipping_phone']
    readonly_fields = ['created_at', 'updated_at', 'delivered_at', 'total_price']
    inlines = [OrderItemInline]
    fieldsets = (
        ('Foydalanuvchi', {
            'fields': ('user',)
        }),
        ('Buyurtma ma\'lumoti', {
            'fields': ('status', 'total_price')
        }),
        ('Yetkazish ma\'lumotlari', {
            'fields':  ('shipping_address', 'shipping_phone')
        }),
        ('Vaqtlar', {
            'fields': ('created_at', 'updated_at', 'delivered_at')
        }),
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price']
    list_filter = ['order__created_at']
    search_fields = ['product__name']
    readonly_fields = ['price']
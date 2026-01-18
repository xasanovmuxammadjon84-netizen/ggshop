from django.contrib import admin
from django.shortcuts import render
from django.urls import path
from .models import Product, Category, ProductReview

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # Ro'yxat ko'rinishi
    list_display = ['name', 'price', 'stock', 'category', 'rating', 'is_active', 'created_at']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    
    # Faqat o'qish uchun maydonlar
    # rating'ni bu yerdan olib tashladik, chunki fieldsets'da tahrirlash imkoni bo'lishi kerak
    readonly_fields = ['created_at', 'updated_at', 'reviews_count']
    
    # Admin formasi tuzilishi
    fieldsets = (
        ('Asosiy ma\'lumot', {
            'fields': ('name', 'description', 'category')
        }),
        ('Narxi va soni', {
            'fields': ('price', 'stock')
        }),
        ('Baho va sharhlar', {
            'fields': ('rating', 'reviews_count') # reviews_count readonly bo'lgani uchun ko'rinadi lekin o'zgarmaydi
        }),
        ('Rasm', {
            'fields': ('image',)
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Vaqtlar', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_site.admin_view(self.dashboard_view)),
        ]
        return custom_urls + urls

    def dashboard_view(self, request):
        return render(request, 'admin/admin_custom.html')

@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['product__name', 'user__username']
    readonly_fields = ['created_at']
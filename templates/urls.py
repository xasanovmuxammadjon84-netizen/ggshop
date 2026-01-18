from django.views.generic import TemplateView

urlpatterns = [
    # Foydalanuvchi sahifasi
    path('', TemplateView.as_view(template_name='index.html')),
    
    # Custom Admin sahifasi
    path('admin-panel/', TemplateView.as_view(template_name='admin_custom.html')),
    
    # Qolgan API yo'llari o'z joyida qoladi
    path('admin/', admin.site.urls),
    path('api/products/', include('products.urls')),
    path('api/orders/', include('orders.urls')),
]
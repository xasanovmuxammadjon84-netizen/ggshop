from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView # Muhim!

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('admin-panel/', TemplateView.as_view(template_name='admin_custom.html'), name='admin_panel'),
    path('admin/', admin.site.urls),
    path('api/products/', include('products.urls')),
    path('api/orders/', include('orders.urls')),
    path('api-auth/', include('rest_framework.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()


router.register(r'promos', views.PromoViewSet, basename='promo')
router.register(r'', views.OrderViewSet, basename='order')

urlpatterns = [
    path('admin-panel/', views.admin_custom, name='admin_custom'),
    
    path('', include(router.urls)),
]
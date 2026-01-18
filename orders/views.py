from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Order, OrderItem, Promo
from .serializers import OrderSerializer, OrderCreateSerializer, OrderItemSerializer, PromoSerializer

# 1. ADMIN TEKSHIRUV FUNKSIYASI
def is_admin(user):
    return user.is_authenticated and user.is_staff

# 2. ADMIN PANEL SAHIFASI (Login va Adminlikni talab qiladi)
@login_required(login_url='/admin/login/') 
@user_passes_test(is_admin, login_url='/admin/login/')
def admin_custom(request):
    return render(request, 'admin_custom.html')

# 3. PROMO VIEWSET (Xavfsiz qilingan)
class PromoViewSet(viewsets.ModelViewSet):
    queryset = Promo.objects.all()
    serializer_class = PromoSerializer
    # Faqat adminlar o'zgartira oladi
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

# 4. ORDER VIEWSET
class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        return OrderSerializer
    
    @action(detail=False, methods=['get'])
    def my_orders(self, request):
        orders = self.get_queryset()
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def mark_as_shipped(self, request, pk=None):
        order = self.get_object()
        order.status = 'shipped'
        order.save()
        return Response(OrderSerializer(order).data)
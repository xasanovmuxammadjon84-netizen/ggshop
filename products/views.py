from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count
from django.db.models.functions import TruncDate

from .models import Product, Category, ProductReview
from .serializers import (
    ProductSerializer, ProductListSerializer,
    CategorySerializer, ProductReviewSerializer
)

class CategoryViewSet(viewsets.ModelViewSet):
    """Kategoriyalar bilan ishlash: Admin o'zgartira oladi, hamma ko'ra oladi"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']: 
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]

class ProductViewSet(viewsets.ModelViewSet):
    """Mahsulotlar API: Qidiruv, Statistika va Sharhlar bilan"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer
        return ProductSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]

    # --- 1. DASHBOARD STATISTIKASI (Grafik uchun) ---
    @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny])
    def stats(self, request):
        """Admin panel uchun umumiy raqamlar va 7 kunlik grafik ma'lumotlari"""
        total_products = Product.objects.count()
        # Bizda 4 xil kategoriya tanlovi bor
        total_categories = 4 
        
        today = timezone.now().date()
        last_7_days = today - timedelta(days=6)
        
        # Bazadan oxirgi 7 kundagi mahsulotlarni sanash
        stats_query = (
            Product.objects.filter(created_at__date__gte=last_7_days)
            .annotate(date=TruncDate('created_at'))
            .values('date')
            .annotate(count=Count('id'))
            .order_by('date')
        )

        mapping = {item['date']: item['count'] for item in stats_query}
        chart_labels = []
        chart_data = []
        
        for i in range(7):
            day = last_7_days + timedelta(days=i)
            chart_labels.append(day.strftime('%d-%b'))
            chart_data.append(mapping.get(day, 0))

        return Response({
            'total_products': total_products,
            'total_categories': total_categories,
            'chart_labels': chart_labels,
            'chart_data': chart_data,
        })

    # --- 2. QIDIRUV VA FILTR (Search) ---
    def get_queryset(self):
        queryset = Product.objects.all()
        search_query = self.request.query_params.get('search', None)
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)
        return queryset

    # --- 3. SHARH QO'SHISH ---
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def add_review(self, request, pk=None):
        product = self.get_object()
        rating = request.data.get('rating')
        comment = request.data.get('comment', '')
        
        if not rating: 
            return Response({'error': 'Reyting kiritilmadi'}, status=400)
        
        review, created = ProductReview.objects.update_or_create(
            product=product,
            user=request.user,
            defaults={'rating': rating, 'comment': comment}
        )
        return Response(ProductReviewSerializer(review).data)

    # --- 4. MAXSUS RO'YXATLAR (Kam qolgan va Saralanganlar) ---
    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        low_stock_products = self.queryset.filter(stock__lte=5)
        return Response(ProductListSerializer(low_stock_products, many=True).data)

    @action(detail=False, methods=['get'])
    def featured(self, request):
        featured_products = self.queryset.order_by('-rating')[:10]
        return Response(ProductListSerializer(featured_products, many=True).data)
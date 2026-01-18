from rest_framework import serializers
from .models import Order, OrderItem
from rest_framework import serializers
from .models import Promo

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_image = serializers.CharField(source='product.image', read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'product_image', 'quantity', 'price']
        read_only_fields = ['id', 'price']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    user_name = serializers.CharField(source='user.username', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'user_name', 'status', 'status_display',
            'total_price', 'shipping_address', 'shipping_phone',
            'items', 'created_at', 'updated_at', 'delivered_at'
        ]
        read_only_fields = ['id', 'user_name', 'total_price', 'created_at', 'updated_at', 'delivered_at']


class OrderCreateSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    
    class Meta: 
        model = Order
        fields = ['shipping_address', 'shipping_phone', 'items']
    
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        user = self.context['request'].user
        
        order = Order.objects.create(user=user, **validated_data)
        
        total = 0
        for item_data in items_data:
            product = item_data['product']
            quantity = item_data['quantity']
            
            # Stock tekshirish
            if product. stock < quantity:
                raise serializers.ValidationError(
                    f"{product.name} - yetarli miqdorda mahsulot yo'q"
                )
            
            price = product.price
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=price
            )
            
            # Stockni kamaytirish
            product.stock -= quantity
            product.save()
            
            total += price * quantity
        
        order. total_price = total
        order.save()
        
        return order

class PromoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promo
        fields = '__all__' 


class PromoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promo
        fields = ['id', 'title', 'subtitle', 'image', 'button_text', 'button_url', 'is_active']
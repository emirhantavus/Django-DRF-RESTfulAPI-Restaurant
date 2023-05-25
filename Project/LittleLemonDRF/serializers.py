from rest_framework import serializers
from .models import MenuItem , Cart , Order , OrderItem

class MenuItemSerializer(serializers.ModelSerializer):
      class Meta:
            model = MenuItem
            fields = ['id','title','price','featured','category']

class CartSerializer(serializers.ModelSerializer):
      class Meta:
            model = Cart
            fields = ['id','quantity','unit_price','price','user','menuitem']
            
class OrderSerializer(serializers.ModelSerializer):
      class Meta:
            model = Order
            fields = ['id','user','delivery_crew','status','total','date']
            
class OrderItemSerializer(serializers.ModelSerializer):
      class Meta:
            model = OrderItem
            fields = ['id','order','menuitem','quantity','unit_price','price']
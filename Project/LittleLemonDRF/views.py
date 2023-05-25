from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view , renderer_classes
from django.core.paginator import Paginator , EmptyPage
from .models import MenuItem , Cart , Order , OrderItem
from .serializers import MenuItemSerializer , CartSerializer ,OrderSerializer , OrderItemSerializer
      
      
from rest_framework.permissions import IsAdminUser
from django.contrib.auth.models import User,Group

@api_view(['GET','POST','DELETE'])
def manager_view(request):
      if(request.user.groups.filter(name='Manager')):
            if request.method == 'GET':
                  managers = Group.objects.get(name='Manager')
                  users = managers.user_set.all().values()
                  return Response(users,status.HTTP_200_OK)
            if request.method == 'POST':
                  username = request.data['username']
                  if username:
                        user = get_object_or_404(User,username=username)
                        managers = Group.objects.get(name='Manager')
                        if request.method == 'POST':
                              managers.user_set.add(user)
                        elif request.method == 'DELETE':
                              managers.user_set.remove(user)
                        return Response({'message':'user added to the manager group'},status.HTTP_201_CREATED)
                  return Response({"message":"error"},status.HTTP_400_BAD_REQUEST)
      
@api_view(['DELETE'])
def delete_manager(request,id):
      id = get_object_or_404(User,pk=id)
      managers = Group.objects.get(name='Manager')
      if(request.user.groups.filter(name='Manager')):
            if request.method == 'DELETE':
                  managers.user_set.remove(id) #secileni sildik
            return Response({'message':'deleted'})
      else:
            return Response({'message':'hata'})
            
@api_view(['GET','POST'])
def delivery_crew_view(request):
      if(request.user.groups.filter(name='Manager')):
            username = request.data['username']
            user = get_object_or_404(User,username=username)
            if request.method == 'GET':
                  managers = Group.objects.get(name='Delivery crew')
                  users = managers.user_set.all().values()
                  return Response(users,status.HTTP_200_OK)
            if request.method == 'POST':
                  if username:
                        delivery_crews = Group.objects.get(name='Delivery crew')
                        delivery_crews.user_set.add(user)
                        return Response({'message':'user added to the delivery crew group'},status.HTTP_201_CREATED)
      else:
            return Response({"message":"error"},status.HTTP_403_FORBIDDEN)
            
@api_view(['DELETE'])
def delete_deliver_crew(request,id):
      id = get_object_or_404(User,pk=id)
      delivery = Group.objects.get(name='Delivery crew')
      if(request.user.groups.filter(name='Manager')):
            if request.method == 'DELETE':
                  delivery.user_set.remove(id) #secileni sildik
            return Response({'message':'deleted'})
      else:
            return Response({'message':'hata'}) 
     
@api_view(['GET','POST','PUT','DELETE'])            
def menu_items(request):
      items = MenuItem.objects.all()
      if (request.user.groups.filter(name='Customer') or request.user.groups.filter(name='Delivery crew')):
            if request.method == 'GET':
                  serialized_item = MenuItemSerializer(items,many=True)
                  return Response(serialized_item.data,status.HTTP_200_OK)
            elif request.method == 'POST' or 'PUT' or 'PATCH' or 'DELETE':
                  return Response({"message":"Denies access"},status.HTTP_403_FORBIDDEN)
            else:
                  return Response({'message':'another error'})        
      elif(request.user.groups.filter(name='Manager')):
            if request.method == 'GET':
                  serialized_item = MenuItemSerializer(items,many=True)
                  return Response(serialized_item.data,status.HTTP_200_OK)
            elif request.method == 'POST':
                  serialized_item = MenuItemSerializer(data=request.data)
                  serialized_item.is_valid(raise_exception=True)
                  serialized_item.save()
                  return Response(serialized_item.validated_data,status.HTTP_201_CREATED)
            else:
                  return Response({'message':'error while posting'})
      elif(request.user.is_superuser):
            serialized_item = MenuItemSerializer(items,many=True)
            return Response(serialized_item.data,status.HTTP_200_OK)                                          
      else:
            return Response({'message':'disarida error'})
      
            
from django.shortcuts import get_object_or_404

@api_view(['GET','POST','PUT','DELETE','PATCH'])            
def single_menu_items(request,id):
      if (request.user.groups.filter(name='Customer') or request.user.groups.filter(name='Delivery crew')):
            if request.method == 'GET':
                  items = MenuItem.objects.get(pk=id)
                  serialized_item = MenuItemSerializer(items)
                  return Response(serialized_item.data,status.HTTP_200_OK)
            elif request.method == 'POST' or 'PUT' or 'PATCH' or 'DELETE':
                  return Response(status.HTTP_403_FORBIDDEN)
            else:
                  return Response({'message':'iceride error'})
      elif(request.user.groups.filter(name='Manager')):
            if request.method == 'GET':
                  items = MenuItem.objects.get(pk=id)
                  serialized_item = MenuItemSerializer(items)
                  return Response(serialized_item.data,status.HTTP_200_OK)
      elif(request.user.groups.filter(name='Manager')):
            if (request.method == 'PUT' or 'PATCH'):
                  item = MenuItem.objects.filter(id=id)
                  serialized_item = MenuItemSerializer(item,data=request.data)
                  if serialized_item.is_valid():
                        serialized_item.save()
                        return Response(serialized_item.data)
                  return Response(serialized_item.errors,status=status.HTTP_400_BAD_REQUEST) 
      elif(request.user.groups.filter(name='Manager')):
            if(request.method == 'DELETE'):
                  MenuItem.objects.filter(pk=id).delete()
                  return Response({"message":"deleted"},status.HTTP_204_NO_CONTENT)
      elif(request.user.is_superuser):
            items = MenuItem.objects.get(pk=id)
            serialized_item = MenuItemSerializer(items)
            return Response(serialized_item.data,status.HTTP_200_OK)  
      else:
            return Response({'message':'disarida error'})
      
@api_view(['POST','GET','DELETE'])
def cart_menu_items(request):
      items = Cart.objects.all()
      if request.method == 'GET':
            if (request.user.groups.filter(name='Customer')):
                  serialized_item = CartSerializer(items,many=True)
                  return Response(serialized_item.data,status.HTTP_200_OK)
            
      elif request.method == 'POST':
                  serialized_item = CartSerializer(data=request.data)
                  serialized_item.is_valid(raise_exception=True)
                  serialized_item.save()
                  return Response(serialized_item.validated_data,status.HTTP_201_CREATED)
            
      elif request.method == 'DELETE':
            carts = Cart.objects.filter(user=request.user) #the user who added new datas.
            carts.delete()
            return Response({"message":"deleted"},status.HTTP_204_NO_CONTENT)
      else:
            return Response({'message':'customer degilsin'})
      
@api_view(['GET','POST'])
def get_orders(request):
      items = Order.objects.all()
      if request.method == 'GET':
            if (request.user.groups.filter(name='Customer')):
                  finduser = Order.objects.filter(user=request.user)#find this user
                  serialized_item = OrderSerializer(finduser,many=True)
                  return Response(serialized_item.data,status.HTTP_200_OK)
            elif(request.user.groups.filter(name='Manager')):
                  serialized_item = OrderSerializer(items,many=True)
                  return Response(serialized_item.data,status.HTTP_200_OK)
            elif(request.user.groups.filter(name='Delivery crew')):
                  finduser = Order.objects.filter(user=request.user)
                  serialized_item = OrderSerializer(finduser,many=True)
                  return Response(serialized_item.data,status.HTTP_200_OK)
            else:
                  return Response({'message':'error'})
      elif request.method == 'POST':
            serialized_item = OrderSerializer(data=request.data)
            serialized_item.is_valid(raise_exception=True)
            serialized_item.save()
            return Response(serialized_item.data,status.HTTP_201_CREATED)
      else:
            Response({'message':'different error'})
            
      
@api_view(['DELETE'])      
def delete_order(request,id):
      order = Order.objects.get(pk=id)
      order.delete()
      return Response({'messaage':'deleted'})
###################################################
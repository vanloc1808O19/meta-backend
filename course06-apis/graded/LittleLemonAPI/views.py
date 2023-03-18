from rest_framework.response import Response
from rest_framework import status, generics
from .models import Cart, Category, MenuItem, Order, OrderItem
from .serializers import CartSerializer, CategorySerializer, MenuItemSerializer, OrderSerializer, OrderItemSerializer, UserSerializer
from django.db.utils import IntegrityError
from rest_framework.request import Request
from rest_framework.views import APIView
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404
from decimal import Decimal
from rest_framework.permissions import IsAdminUser
from .permissions import Manager, DeliveryCrew, Customer
from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter

# Create your views here.
class CategoryListView(generics.ListCreateAPIView):

    @property
    def permission_classes(self):
        if self.request.method == 'GET':
            return [IsAdminUser|Customer|Manager]
        elif self.request.method == 'POST':
            return [IsAdminUser|Manager]

    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class MenuItemListView(generics.ListCreateAPIView):
    @property
    def permission_classes(self):
        if self.request.method == 'GET':
            return [IsAdminUser|Customer|Manager]
        elif self.request.method == 'POST':
            return [IsAdminUser|Manager]
        
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    ordering_fields = ['price', 'title']
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    filterset_fields = ['category', 'featured']

    def create(self, request, *args, **kwargs):    
        try:
            return super().create(request, *args, **kwargs)
        except IntegrityError as e:
            return Response({'Error': 'Integrity Error'}, status=status.HTTP_400_BAD_REQUEST)

class MenuItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser | Manager]
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    def update(self, request, *args, **kwargs):
        try:
            return super().update(request, *args, **kwargs)
        except IntegrityError as e:
            return Response({'Error': 'Integrity Error'}, status=status.HTTP_400_BAD_REQUEST)
        
    def partial_update(self, request, *args, **kwargs):
        try:
            return super().partial_update(request, *args, **kwargs)
        except IntegrityError as e:
            return Response({'Error': 'Integrity Error'}, status=status.HTTP_400_BAD_REQUEST)
        
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
        
class UserGroupListView(APIView):
    permission_classes = [Manager | IsAdminUser]

    def get(self, request, group_name):
        users = User.objects.filter(groups__name=group_name)
        serialized_users = UserSerializer(users, many=True)

        return Response(serialized_users.data, status=status.HTTP_200_OK)
        
    def post(self, request, group_name):
        username = request.data.get('username')
        
        if username:
            user = get_object_or_404(User, username=username)
            group =  Group.objects.get(name=group_name)

            group.user_set.add(user)

            return Response({'Message': 'User added to group'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'Error': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)
        
class UserGroupDestroyView(APIView):
    permission_classes = [Manager | IsAdminUser]

    def delete(self, request, group_name, user_id):
        user = get_object_or_404(User, pk=user_id)

        if user.groups.filter(name=group_name).exists():
            group =  Group.objects.get(name=group_name)

            group.user_set.remove(user)

            return Response({'Message': f'User removed from {group_name} group'}, status=status.HTTP_200_OK)
        else:
            return Response({'Message': f'User does not belong to {group_name} group'}, status=status.HTTP_400_BAD_REQUEST)
        
class CartListView(APIView):
    permission_classes = [Customer]
    
    def get(self, request):
        cart_items = Cart.objects.filter(user=request.user)
        serialized_cart_items = CartSerializer(cart_items, many=True)
        return Response(serialized_cart_items.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        menuitem_id = request.data.get('menuitem')
        if menuitem_id:
            try:
                cartitem = Cart.objects.get(menuitem_id=menuitem_id, user_id=request.user.id)
                cartitem.quantity += 1
                cartitem.price += cartitem.unit_price
                cartitem.save()
            except Cart.DoesNotExist:
                menuitem = get_object_or_404(MenuItem, id=menuitem_id)
                cartitem = Cart(menuitem=menuitem, user=request.user, quantity=1, price=menuitem.price, unit_price=menuitem.price)
                cartitem.save()

            serialized_cart_item = CartSerializer(cartitem)

            return Response(serialized_cart_item.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'Error': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request):
        Cart.objects.filter(user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class OrderListView(APIView):

    @property
    def permission_classes(self):
        if self.request.method == 'GET':
            return [Manager|Customer|DeliveryCrew]
        elif self.request.method == 'POST':
            return [Customer]
        
    def get(self, request):
        ordering =  request.query_params.get('ordering')

        if request.user.groups.filter(name="manager").exists():
            orders = Order.objects.all()
            serialized_orders = self.serialize_orders(orders)
            
            return Response(serialized_orders, status=status.HTTP_200_OK)
        elif request.user.groups.filter(name="delivery-crew").exists():
            orders = Order.objects.filter(delivery_crew=request.user)
            serialized_orders = self.serialize_orders(orders)
            
            return Response(serialized_orders, status=status.HTTP_200_OK)
        else:
            orders = Order.objects.filter(user=request.user)
            if ordering:
                orders = orders.order_by(*ordering.split(','))
            serialized_orders = self.serialize_orders(orders)
            
            return Response(serialized_orders, status=status.HTTP_200_OK)

    def serialize_orders(self, orders):
        serialized_orders = []
        for order in orders:
            order_items = OrderItem.objects.filter(order=order)
            serialized_order_items = OrderItemSerializer(order_items, many=True)
            serialized_orders.append(OrderSerializer(order, context={'order_items': serialized_order_items.data}).data)

        return serialized_orders

    def post(self, request):
        cart_items = Cart.objects.filter(user=request.user)
        if cart_items:
            order_total = Decimal(0)
            for item in cart_items:
                order_total += item.price

            order = Order(user=request.user,total=order_total)
            order.save()

            for item in cart_items:
                OrderItem.objects.create(order=order, menuitem = item.menuitem, quantity=item.quantity, unit_price=item.unit_price,price=item.price)

            cart_items.delete()

            serialized_order = OrderSerializer(order)
            
            return Response(serialized_order.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'Message': 'No items in cart'}, status=status.HTTP_400_BAD_REQUEST)
        
class OrderDetailView(APIView):
    
    @property
    def permission_classes(self):
        if self.request.method == 'GET':
            return [Customer]
        elif self.request.method == 'DELETE':
            return [Manager]
        elif self.request.method == 'PATCH':
            return [Manager|DeliveryCrew]
        
    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        order_items = OrderItem.objects.filter(order=order)
        serialized_order_items = OrderItemSerializer(order_items, many=True)
        serialized_order = OrderSerializer(order, context={'order_items': serialized_order_items.data})

        return Response(serialized_order.data, status=status.HTTP_200_OK)
        
    def delete(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        order.delete()

        return Response({'message': 'Order deleted'}, status=status.HTTP_200_OK)
        
    def patch(self, request, order_id):
        if request.user.groups.filter(name="manager").exists():
            delivery_crew_id = request.data.get('delivery_crew')
        
            if 'status' in request.data  or 'delivery_crew' in request.data:
                order = get_object_or_404(Order, id=order_id)

                if 'status' in request.data:
                    if request.data['status'] in [0, 1, True, False]:
                        order.status = request.data['status']
                    else:
                        return Response({'message': 'Status can accept only boolean values'}, status=status.HTTP_400_BAD_REQUEST)
                
                if 'delivery_crew' in request.data:
                    if request.data['delivery_crew'] is not None:
                        delivery_crew = get_object_or_404(User, id=delivery_crew_id)
                        if delivery_crew.groups.filter(name="delivery-crew").exists():
                            order.delivery_crew = delivery_crew
                        else:
                            return Response({'message': 'Given user is not a delivery crew'}, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        order.delivery_crew = None
                
                order.save()

                return Response(OrderSerializer(order).data, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)
        elif request.user.groups.filter(name="delivery-crew").exists():
            if 'status' in request.data:
                order = get_object_or_404(Order, id=order_id)

                if request.data['status'] in [0, 1, True, False]:
                    order.status = request.data['status']
                else:
                    return Response({'message': 'Status can accept only boolean values'}, status=status.HTTP_400_BAD_REQUEST)
                order.save()

                return Response(OrderSerializer(order).data, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)
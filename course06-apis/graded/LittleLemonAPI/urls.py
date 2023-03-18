from django.urls import path
from .views import MenuItemListView, MenuItemDetailView, CategoryListView, UserGroupListView, UserGroupDestroyView, CartListView, OrderListView, OrderDetailView

urlpatterns = [
    path('categories', CategoryListView.as_view(), name='category-list'),
    path('menu-items', MenuItemListView.as_view(), name='menu-items-list'),
    path('menu-items/<int:pk>', MenuItemDetailView.as_view(), name='menu-items-detail'),
    path('groups/<str:group_name>/users', UserGroupListView.as_view(), name='user-groups'),
    path('groups/<str:group_name>/users/<int:user_id>', UserGroupDestroyView.as_view(), name='user-group'),
    path('cart/menu-items', CartListView.as_view(), name='cart-menu-items'),
    path('orders', OrderListView.as_view(), name='orders'),
    path('orders/<int:order_id>', OrderDetailView.as_view(), name='order-details')
]
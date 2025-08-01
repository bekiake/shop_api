from django.urls import path
from orders.views import OrderListCreateView, OrderDetailView, AdminOrderListView, AdminOrderDetailView, AdminOrderStatusUpdateView

urlpatterns = [
    path('', OrderListCreateView.as_view(), name='order_list_create'),
    path('<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    path('admin/', AdminOrderListView.as_view(), name='admin_order_list'),
    path('admin/<int:pk>/', AdminOrderDetailView.as_view(), name='admin_order_detail'),
    path('admin/<int:pk>/status/', AdminOrderStatusUpdateView.as_view(), name='admin_order_status_update'),

]

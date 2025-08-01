from django.urls import path
from cart.views import CartView, CartItemUpdateDeleteView

urlpatterns = [
    path('', CartView.as_view(), name='cart'),
    path('item/<int:pk>/', CartItemUpdateDeleteView.as_view(), name='cart_item_update_delete'),
]

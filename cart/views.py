from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from cart.models import Cart, CartItem
from cart.serializers import CartSerializer, CartItemCreateUpdateSerializer
from drf_yasg.utils import swagger_auto_schema  # qo‘shildi

class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get_cart(self, user):
        cart, created = Cart.objects.get_or_create(user=user)
        return cart

    # Savatni ko‘rish
    def get(self, request):
        cart = self.get_cart(request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    # Mahsulot qo‘shish
    @swagger_auto_schema(request_body=CartItemCreateUpdateSerializer)
    def post(self, request):
        cart = self.get_cart(request.user)
        serializer = CartItemCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.validated_data['product']
            quantity = serializer.validated_data['quantity']

            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            if not created:
                cart_item.quantity += quantity
            else:
                cart_item.quantity = quantity
            cart_item.save()
            return Response({"detail": "Mahsulot savatga qo‘shildi"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CartItemUpdateDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    # Miqdorni yangilash
    @swagger_auto_schema(request_body=CartItemCreateUpdateSerializer)
    def put(self, request, pk):
        try:
            item = CartItem.objects.get(pk=pk, cart__user=request.user)
        except CartItem.DoesNotExist:
            return Response({"detail": "Mahsulot savatda topilmadi"}, status=status.HTTP_404_NOT_FOUND)
        serializer = CartItemCreateUpdateSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Miqdor yangilandi"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Mahsulotni o‘chirish
    def delete(self, request, pk):
        try:
            item = CartItem.objects.get(pk=pk, cart__user=request.user)
        except CartItem.DoesNotExist:
            return Response({"detail": "Mahsulot savatda topilmadi"}, status=status.HTTP_404_NOT_FOUND)
        item.delete()
        return Response({"detail": "Mahsulot o‘chirildi"}, status=status.HTTP_204_NO_CONTENT)

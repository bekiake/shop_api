from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiResponse

from cart.models import Cart, CartItem
from cart.serializers import CartSerializer, CartItemCreateUpdateSerializer

@extend_schema(tags=['Savat'])
class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get_cart(self, user):
        cart, created = Cart.objects.get_or_create(user=user)
        return cart

    @extend_schema(
        responses=CartSerializer,
        summary="Savatni ko‘rish",
        description="Joriy foydalanuvchining savatini ko‘rsatadi."
    )
    def get(self, request):
        cart = self.get_cart(request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    @extend_schema(
        request=CartItemCreateUpdateSerializer,
        responses={201: OpenApiResponse(description="Mahsulot savatga qo‘shildi")},
        summary="Mahsulot qo‘shish",
        description="Foydalanuvchining savatiga yangi mahsulot qo‘shadi yoki mavjudining miqdorini oshiradi."
    )
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

@extend_schema(tags=['Savat'])
class CartItemUpdateDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=CartItemCreateUpdateSerializer,
        responses={200: OpenApiResponse(description="Miqdor yangilandi")},
        summary="Savatdagi mahsulot miqdorini yangilash",
        description="Foydalanuvchi savatidagi tanlangan mahsulot miqdorini yangilaydi."
    )
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

    @extend_schema(
        responses={204: OpenApiResponse(description="Mahsulot o‘chirildi")},
        summary="Mahsulotni o‘chirish",
        description="Foydalanuvchi savatidan mahsulotni o‘chiradi."
    )
    def delete(self, request, pk):
        try:
            item = CartItem.objects.get(pk=pk, cart__user=request.user)
        except CartItem.DoesNotExist:
            return Response({"detail": "Mahsulot savatda topilmadi"}, status=status.HTTP_404_NOT_FOUND)
        item.delete()
        return Response({"detail": "Mahsulot o‘chirildi"}, status=status.HTTP_204_NO_CONTENT)

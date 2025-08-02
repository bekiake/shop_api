from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse

from orders.models import Order
from orders.serializers import OrderSerializer, OrderStatusUpdateSerializer

# --------- Foydalanuvchi buyurtmalari ---------
@extend_schema(tags=['Buyurtmalar'])
class OrderListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        parameters=[
            OpenApiParameter(name='status', description="Holat bo‘yicha filter", required=False, type=str),
            OpenApiParameter(name='page', description="Sahifa raqami", required=False, type=int),
            OpenApiParameter(name='page_size', description="Sahifadagi elementlar soni", required=False, type=int),
        ],
        responses=OpenApiResponse(response=OrderSerializer(many=True), description="Foydalanuvchi buyurtmalari ro‘yxati"),
        summary="Foydalanuvchi buyurtmalari ro‘yxati",
        description="Joriy foydalanuvchining barcha buyurtmalari ro‘yxatini chiqaradi. Filtrlash va sahifalash qo‘llab-quvvatlanadi."
    )
    def get(self, request):
        status_filter = request.query_params.get('status')
        orders = Order.objects.filter(user=request.user)
        if status_filter:
            orders = orders.filter(status=status_filter)

        # Sahifalash
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 10))
        start = (page - 1) * page_size
        end = start + page_size
        total = orders.count()
        orders = orders[start:end]

        serializer = OrderSerializer(orders, many=True)
        return Response({
            "total": total,
            "page": page,
            "page_size": page_size,
            "results": serializer.data
        })

@extend_schema(tags=['Buyurtmalar'])
class OrderDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        parameters=[
            OpenApiParameter(name='pk', location=OpenApiParameter.PATH, description="Buyurtma ID", required=True, type=int),
        ],
        responses=OrderSerializer,
        summary="Foydalanuvchi buyurtma tafsilotlari",
        description="Foydalanuvchining o‘ziga tegishli bitta buyurtma ma'lumotini ko‘rsatadi."
    )
    def get(self, request, pk):
        try:
            order = Order.objects.get(pk=pk, user=request.user)
        except Order.DoesNotExist:
            return Response({"detail": "Buyurtma topilmadi"}, status=status.HTTP_404_NOT_FOUND)
        serializer = OrderSerializer(order)
        return Response(serializer.data)


# --------- Admin buyurtmalari ---------
@extend_schema(tags=['Admin'])
class AdminOrderListView(APIView):
    permission_classes = [IsAdminUser]

    @extend_schema(
        parameters=[
            OpenApiParameter(name='status', description="Holat bo‘yicha filter: processing, shipped, delivered", required=False, type=str),
        ],
        responses=OrderSerializer(many=True),
        summary="Admin uchun barcha buyurtmalar",
        description="Barcha foydalanuvchilarning buyurtmalarini ko‘rish imkoniyati."
    )
    def get(self, request):
        status_filter = request.query_params.get('status')
        orders = Order.objects.all()
        if status_filter:
            orders = orders.filter(status=status_filter)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

@extend_schema(tags=['Admin'])
class AdminOrderDetailView(APIView):
    permission_classes = [IsAdminUser]

    @extend_schema(
        responses=OrderSerializer,
        summary="Admin uchun bitta buyurtma",
        description="Admin bitta buyurtma tafsilotlarini ko‘rishi mumkin."
    )
    def get(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response({"detail": "Buyurtma topilmadi"}, status=status.HTTP_404_NOT_FOUND)
        serializer = OrderSerializer(order)
        return Response(serializer.data)

@extend_schema(tags=['Admin'])
class AdminOrderStatusUpdateView(APIView):
    permission_classes = [IsAdminUser]

    @extend_schema(
        request=OrderStatusUpdateSerializer,
        responses={200: OpenApiResponse(description="Buyurtma holati yangilandi"), 400: OpenApiResponse(description="Xato ma'lumot")},
        summary="Admin buyurtma holatini yangilash",
        description="Admin buyurtma holatini (processing, shipped, delivered) yangilaydi."
    )
    def put(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response({"detail": "Buyurtma topilmadi"}, status=status.HTTP_404_NOT_FOUND)
        serializer = OrderStatusUpdateSerializer(data=request.data)
        if serializer.is_valid():
            order.status = serializer.validated_data['status']
            order.save()
            return Response({"detail": "Holat yangilandi"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

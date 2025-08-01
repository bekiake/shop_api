from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from orders.models import Order, OrderItem
from orders.serializers import OrderSerializer, OrderCreateSerializer, OrderStatusUpdateSerializer
from cart.models import Cart, CartItem
from rest_framework.permissions import IsAdminUser

class OrderListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('status', openapi.IN_QUERY, description="Holat bo‘yicha filter", type=openapi.TYPE_STRING),
            openapi.Parameter('page', openapi.IN_QUERY, description="Sahifa raqami", type=openapi.TYPE_INTEGER),
            openapi.Parameter('page_size', openapi.IN_QUERY, description="Sahifadagi elementlar soni", type=openapi.TYPE_INTEGER),
        ]
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

class OrderDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'pk', openapi.IN_PATH, 
                description="Buyurtma ID (yo‘lda beriladi)", 
                type=openapi.TYPE_INTEGER
            )
        ]
    )
    def get(self, request, pk):
        try:
            order = Order.objects.get(pk=pk, user=request.user)
        except Order.DoesNotExist:
            return Response({"detail": "Buyurtma topilmadi"}, status=status.HTTP_404_NOT_FOUND)
        serializer = OrderSerializer(order)
        return Response(serializer.data)


class AdminOrderListView(APIView):
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'status',
                openapi.IN_QUERY,
                description="Holat bo‘yicha filter: processing, shipped, delivered",
                type=openapi.TYPE_STRING
            )
        ]
    )
    def get(self, request):
        status_filter = request.query_params.get('status')
        orders = Order.objects.all()
        if status_filter:
            orders = orders.filter(status=status_filter)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


class AdminOrderDetailView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response({"detail": "Buyurtma topilmadi"}, status=status.HTTP_404_NOT_FOUND)
        serializer = OrderSerializer(order)
        return Response(serializer.data)


class AdminOrderStatusUpdateView(APIView):
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(request_body=OrderStatusUpdateSerializer)
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
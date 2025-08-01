from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from products.models import Product, Category, Tag
from products.serializers import (
    ProductSerializer,
    ProductCreateUpdateSerializer,
    CategorySerializer,
    TagSerializer
)

# --------------------- Mijozlar uchun API ---------------------

class ProductListView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('category', openapi.IN_QUERY, description="Toifa ID bo‘yicha filter", type=openapi.TYPE_INTEGER),
            openapi.Parameter('tag', openapi.IN_QUERY, description="Teg ID bo‘yicha filter", type=openapi.TYPE_INTEGER),
            openapi.Parameter('price_min', openapi.IN_QUERY, description="Minimal narx", type=openapi.TYPE_NUMBER),
            openapi.Parameter('price_max', openapi.IN_QUERY, description="Maksimal narx", type=openapi.TYPE_NUMBER),
            openapi.Parameter('search', openapi.IN_QUERY, description="Nomi yoki tavsifi bo‘yicha qidiruv", type=openapi.TYPE_STRING),
            openapi.Parameter('order_by', openapi.IN_QUERY, description="Tartiblash: price, -price, name, -name", type=openapi.TYPE_STRING),
            openapi.Parameter('page', openapi.IN_QUERY, description="Sahifa raqami", type=openapi.TYPE_INTEGER),
            openapi.Parameter('page_size', openapi.IN_QUERY, description="Har bir sahifadagi elementlar soni", type=openapi.TYPE_INTEGER),
        ]
    )
    def get(self, request):
        queryset = Product.objects.all()

        # Filtrlash
        category = request.query_params.get('category')
        tag = request.query_params.get('tag')
        price_min = request.query_params.get('price_min')
        price_max = request.query_params.get('price_max')
        search = request.query_params.get('search')
        order_by = request.query_params.get('order_by')

        if category:
            queryset = queryset.filter(category_id=category)
        if tag:
            queryset = queryset.filter(tags__id=tag)
        if price_min:
            queryset = queryset.filter(price__gte=price_min)
        if price_max:
            queryset = queryset.filter(price__lte=price_max)
        if search:
            queryset = queryset.filter(Q(name__icontains=search) | Q(description__icontains=search))
        if order_by in ['price', '-price', 'name', '-name']:
            queryset = queryset.order_by(order_by)

        # Sahifalash
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 10))
        start = (page - 1) * page_size
        end = start + page_size
        total = queryset.count()
        queryset = queryset[start:end]

        serializer = ProductSerializer(queryset, many=True)
        return Response({
            "total": total,
            "page": page,
            "page_size": page_size,
            "results": serializer.data
        })


class ProductDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({"detail": "Mahsulot topilmadi"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product)
        return Response(serializer.data)


class CategoryListCreateView(APIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser()]
        return [AllowAny()]

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=CategorySerializer)
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            category = serializer.save()
            return Response(CategorySerializer(category).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# --------------------- Admin uchun API ---------------------

class ProductAdminView(APIView):
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(request_body=ProductCreateUpdateSerializer)
    def post(self, request):
        serializer = ProductCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.save()
            return Response(ProductSerializer(product).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=ProductCreateUpdateSerializer)
    def put(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({"detail": "Mahsulot topilmadi"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductCreateUpdateSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            product = serializer.save()
            return Response(ProductSerializer(product).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({"detail": "Mahsulot topilmadi"}, status=status.HTTP_404_NOT_FOUND)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryDetailView(APIView):
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(request_body=CategorySerializer)
    def put(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response({"detail": "Toifa topilmadi"}, status=status.HTTP_404_NOT_FOUND)
        serializer = CategorySerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            category = serializer.save()
            return Response(CategorySerializer(category).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response({"detail": "Toifa topilmadi"}, status=status.HTTP_404_NOT_FOUND)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TagListCreateView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=TagSerializer)
    def post(self, request):
        serializer = TagSerializer(data=request.data)
        if serializer.is_valid():
            tag = serializer.save()
            return Response(TagSerializer(tag).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TagDetailView(APIView):
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(request_body=TagSerializer)
    def put(self, request, pk):
        try:
            tag = Tag.objects.get(pk=pk)
        except Tag.DoesNotExist:
            return Response({"detail": "Teg topilmadi"}, status=status.HTTP_404_NOT_FOUND)
        serializer = TagSerializer(tag, data=request.data, partial=True)
        if serializer.is_valid():
            tag = serializer.save()
            return Response(TagSerializer(tag).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            tag = Tag.objects.get(pk=pk)
        except Tag.DoesNotExist:
            return Response({"detail": "Teg topilmadi"}, status=status.HTTP_404_NOT_FOUND)
        tag.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

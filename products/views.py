from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django.db.models import Q
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter

from products.models import Product, Category, Tag
from products.serializers import (
    ProductSerializer,
    ProductCreateUpdateSerializer,
    CategorySerializer,
    TagSerializer
)

# --------------------- Mijozlar uchun API ---------------------
@extend_schema(tags=['Mahsulotlar'])
class ProductListView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        parameters=[
            OpenApiParameter(name='category', description="Toifa ID bo‘yicha filter", required=False, type=int),
            OpenApiParameter(name='tag', description="Teg ID bo‘yicha filter", required=False, type=int),
            OpenApiParameter(name='price_min', description="Minimal narx", required=False, type=float),
            OpenApiParameter(name='price_max', description="Maksimal narx", required=False, type=float),
            OpenApiParameter(name='search', description="Nomi yoki tavsifi bo‘yicha qidiruv", required=False, type=str),
            OpenApiParameter(name='order_by', description="Tartiblash: price, -price, name, -name", required=False, type=str),
            OpenApiParameter(name='page', description="Sahifa raqami", required=False, type=int),
            OpenApiParameter(name='page_size', description="Har bir sahifadagi elementlar soni", required=False, type=int),
        ],
        responses=OpenApiResponse(response=ProductSerializer(many=True), description="Mahsulotlar ro‘yxati"),
        summary="Mahsulotlar ro‘yxati",
        description="Mahsulotlarni filtrlash, qidirish va tartiblash imkoniyati bilan ro‘yxatini qaytaradi."
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

@extend_schema(tags=['Mahsulotlar'])
class ProductDetailView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        responses=ProductSerializer,
        summary="Mahsulot tafsiloti",
        description="Mahsulotning to‘liq ma'lumotlarini qaytaradi."
    )
    def get(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({"detail": "Mahsulot topilmadi"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

@extend_schema(tags=['Mahsulotlar'])
class CategoryListCreateView(APIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser()]
        return [AllowAny()]

    @extend_schema(
        responses=CategorySerializer(many=True),
        summary="Toifalar ro‘yxati",
        description="Barcha mavjud toifalar ro‘yxatini qaytaradi."
    )
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    @extend_schema(
        tags=['Admin'],
        request=CategorySerializer,
        responses=CategorySerializer,
        summary="Toifa yaratish (Admin)",
        description="Yangi toifa yaratadi."
    )
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            category = serializer.save()
            return Response(CategorySerializer(category).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# --------------------- Admin uchun API ---------------------
@extend_schema(tags=['Admin'])
class ProductAdminView(APIView):
    permission_classes = [IsAdminUser]

    @extend_schema(
        request=ProductCreateUpdateSerializer,
        responses=ProductSerializer,
        summary="Mahsulot yaratish (Admin)",
        description="Adminlar uchun yangi mahsulot yaratadi."
    )
    def post(self, request):
        serializer = ProductCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.save()
            return Response(ProductSerializer(product).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        request=ProductCreateUpdateSerializer,
        responses=ProductSerializer,
        summary="Mahsulotni yangilash (Admin)",
        description="Adminlar uchun mavjud mahsulot ma'lumotlarini yangilaydi."
    )
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

    @extend_schema(
        responses={204: OpenApiResponse(description="Mahsulot o‘chirildi")},
        summary="Mahsulotni o‘chirish (Admin)",
        description="Adminlar uchun mahsulotni o‘chiradi."
    )
    def delete(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({"detail": "Mahsulot topilmadi"}, status=status.HTTP_404_NOT_FOUND)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@extend_schema(tags=['Admin'])
class CategoryDetailView(APIView):
    permission_classes = [IsAdminUser]

    @extend_schema(
        request=CategorySerializer,
        responses=CategorySerializer,
        summary="Toifani yangilash (Admin)",
        description="Adminlar uchun mavjud toifani yangilaydi."
    )
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

    @extend_schema(
        responses={204: OpenApiResponse(description="Toifa o‘chirildi")},
        summary="Toifani o‘chirish (Admin)",
        description="Adminlar uchun toifani o‘chiradi."
    )
    def delete(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response({"detail": "Toifa topilmadi"}, status=status.HTTP_404_NOT_FOUND)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@extend_schema(tags=['Admin'])
class TagListCreateView(APIView):
    permission_classes = [IsAdminUser]

    @extend_schema(
        responses=TagSerializer(many=True),
        summary="Teglar ro‘yxati (Admin)",
        description="Barcha mavjud teglarni ro‘yxatini qaytaradi."
    )
    def get(self, request):
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)

    @extend_schema(
        request=TagSerializer,
        responses=TagSerializer,
        summary="Yangi teg yaratish (Admin)",
        description="Adminlar uchun yangi teg yaratadi."
    )
    def post(self, request):
        serializer = TagSerializer(data=request.data)
        if serializer.is_valid():
            tag = serializer.save()
            return Response(TagSerializer(tag).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(tags=['Admin'])
class TagDetailView(APIView):
    permission_classes = [IsAdminUser]

    @extend_schema(
        request=TagSerializer,
        responses=TagSerializer,
        summary="Tegni yangilash (Admin)",
        description="Adminlar uchun mavjud tegni yangilaydi."
    )
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

    @extend_schema(
        responses={204: OpenApiResponse(description="Teg o‘chirildi")},
        summary="Tegni o‘chirish (Admin)",
        description="Adminlar uchun tegni o‘chiradi."
    )
    def delete(self, request, pk):
        try:
            tag = Tag.objects.get(pk=pk)
        except Tag.DoesNotExist:
            return Response({"detail": "Teg topilmadi"}, status=status.HTTP_404_NOT_FOUND)
        tag.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

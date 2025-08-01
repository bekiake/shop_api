from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework import status
from users.serializers import LoginSerializer, RegisterSerializer, AdminUserSerializer
from users.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema, OpenApiResponse


class RegisterView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=RegisterSerializer,
        responses={
            201: OpenApiResponse(description="Foydalanuvchi muvaffaqiyatli ro‘yxatdan o‘tdi"),
            400: OpenApiResponse(description="Xato: noto‘g‘ri ma'lumotlar")
        },
        summary="Foydalanuvchini ro'yxatdan o'tkazish",
        description="Yangi foydalanuvchini ro'yxatdan o'tkazib, unga JWT token qaytaradi."
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "user": {
                        "id": user.id,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "email": user.email,
                        "phone": user.phone
                    },
                    "tokens": {
                        "refresh": str(refresh),
                        "access": str(refresh.access_token)
                    }
                }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=LoginSerializer,
        responses={
            200: OpenApiResponse(description="Muvaffaqiyatli login va JWT token qaytaradi"),
            400: OpenApiResponse(description="Xato: noto‘g‘ri login yoki parol")
        },
        summary="Foydalanuvchini login qilish",
        description="Login qilganda foydalanuvchiga JWT token qaytaradi."
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminUserListView(APIView):
    permission_classes = [IsAdminUser]

    @extend_schema(
        responses=AdminUserSerializer(many=True),
        summary="Barcha foydalanuvchilar ro‘yxati (Admin)",
        description="Adminlar uchun barcha foydalanuvchilar ro‘yxatini chiqaradi."
    )
    def get(self, request):
        users = User.objects.all()
        serializer = AdminUserSerializer(users, many=True)
        return Response(serializer.data)


class AdminUserDetailView(APIView):
    permission_classes = [IsAdminUser]

    @extend_schema(
        responses=AdminUserSerializer,
        summary="Bitta foydalanuvchi haqida ma'lumot (Admin)",
        description="Adminlar uchun bitta foydalanuvchi ma'lumotini chiqaradi."
    )
    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"detail": "Foydalanuvchi topilmadi"}, status=status.HTTP_404_NOT_FOUND)
        serializer = AdminUserSerializer(user)
        return Response(serializer.data)

    @extend_schema(
        request=AdminUserSerializer,
        responses=AdminUserSerializer,
        summary="Foydalanuvchi ma'lumotini yangilash (Admin)",
        description="Adminlar uchun foydalanuvchi ma'lumotlarini yangilash imkoniyati."
    )
    def put(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"detail": "Foydalanuvchi topilmadi"}, status=status.HTTP_404_NOT_FOUND)
        serializer = AdminUserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            user = serializer.save()
            return Response(AdminUserSerializer(user).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        responses={204: OpenApiResponse(description="Foydalanuvchi o‘chirildi")},
        summary="Foydalanuvchini o‘chirish (Admin)",
        description="Admin foydalanuvchini o‘chirish imkoniyatiga ega."
    )
    def delete(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"detail": "Foydalanuvchi topilmadi"}, status=status.HTTP_404_NOT_FOUND)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

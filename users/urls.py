from django.urls import path
from users.views import RegisterView, LoginView, AdminUserListView, AdminUserDetailView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('admin/', AdminUserListView.as_view(), name='admin_user_list'),
    path('admin/<int:pk>/', AdminUserDetailView.as_view(), name='admin_user_detail'),
]
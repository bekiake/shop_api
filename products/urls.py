from django.urls import path
from .views import (
    ProductListView, ProductDetailView, ProductAdminView,
    CategoryListCreateView, CategoryDetailView,
    TagListCreateView, TagDetailView
)

urlpatterns = [
    # -------- Mijozlar uchun --------
    path('', ProductListView.as_view(), name='product_list'),                        
    path('<int:pk>/', ProductDetailView.as_view(), name='product_detail'),          
    path('categories/', CategoryListCreateView.as_view(), name='category_list'),  

    # -------- Adminlar uchun --------
    path('admin/', ProductAdminView.as_view(), name='product_create'),              
    path('admin/<int:pk>/', ProductAdminView.as_view(), name='product_update_delete'), 
    path('admin/categories/<int:pk>/', CategoryDetailView.as_view(), name='category_update_delete'), 
    path('admin/tags/', TagListCreateView.as_view(), name='tag_list_create'),         
    path('admin/tags/<int:pk>/', TagDetailView.as_view(), name='tag_update_delete'), 
]

from django.urls import path

from . import views

urlpatterns = [
    path('products/', views.products_list_create_view),
    path('products/<int:id>/update/', views.products_update_view),
    path('<int:pk>/delete/', views.products_destroy_view),
    path('products/<int:pk>/', views.products_detail_view),
    path('branches/', views.branches_listcreate_view),
    path('branches/<int:pk>/update/', views.branches_update_view),
    path('branches/<int:id>/', views.branches_detail_view),
    path('users/', views.users_listcreate_view),
    path('users/<int:pk>/', views.users_detail_view)
]
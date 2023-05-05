from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_products, name='products'),
    path('<int:product_id>/', views.product_detail, name='product_detail'),
    path('add/', views.add_product, name='add_product'),
    path('edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path(
        'delete/<int:product_id>/',
        views.delete_product,
        name='delete_product'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path(
        'add_to_wishlist/<int:product_id>/<int:user_id>',
        views.add_to_wishlist,
        name='add_to_wishlist'),
    path(
        'remove_from_wishlist/<int:wishlist_id>/',
        views.remove_from_wishlist,
        name='remove_from_wishlist'),
    path(
        'add_to_wishlist_all/<int:product_id>/<int:user_id>',
        views.add_to_wishlist_all_products,
        name='add_to_wishlist_all'
    ),
    path(
        'remove_from_wishlist_all/<int:product_id>/<int:user_id>',
        views.remove_from_wishlist_all_products,
        name='remove_from_wishlist_all'
    ),
]

from django.urls import path
from .views import admin, collection, customer, product

urlpatterns = [
    path('', admin.admin_home, name='admin_home'),
    path('collections/', collection.collection_list, name='collection_list'),
    path('collections/<int:pk>/', collection.collection_detail,
         name='collection_detail'),
    path('collections/new/', collection.collection_create,
         name='collection_create'),
    path('collections/<int:pk>/edit/',
         collection.collection_update, name='collection_update'),
    path('collections/<int:pk>/delete/',
         collection.collection_delete, name='collection_delete'),

    path('products/', product.product_list, name='product_list'),
    path('products/<int:pk>/', product.product_detail, name='product_detail'),
    path('products/new/', product.product_create, name='product_create'),
    path('products/<int:pk>/edit/', product.product_update, name='product_update'),
    path('products/<int:pk>/delete/',
         product.product_delete, name='product_delete'),

    path('images/', product.create_image, name='create_image'),
    path('images/<int:pk>/', product.get_image, name='get_image'),
    path('images/<int:pk>/delete/', product.delete_image, name='delete_image'),

    path('customers/', customer.customer_list, name='customer_list'),
    path('customers/<int:pk>/', customer.customer_detail, name='customer_detail'),
    path('customers/new/', customer.customer_create, name='customer_create'),
    path('customers/<int:pk>/edit/',
         customer.customer_update, name='customer_update'),
    path('customers/<int:pk>/delete/',
         customer.customer_delete, name='customer_delete'),
]

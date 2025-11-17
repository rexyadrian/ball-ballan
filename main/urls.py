from django.urls import path
from main.views import (
    show_main,
    register,
    login_user,
    logout_user,
    add_product,
    show_product,
    edit_product,
    delete_product,
    show_xml,
    show_json,
    show_xml_by_id,
    show_json_by_id,
    add_product_ajax
)

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('products/xml/', show_xml, name='show_xml'),
    path('products/json/', show_json, name='show_json'),
    path('products/xml/<str:id>/', show_xml_by_id, name='show_xml_by_id'),
    path('products/json/<str:id>/', show_json_by_id, name='show_json_by_id'),
    path('products/add/', add_product, name='add_product'),
    path('products/<str:id>/', show_product, name='show_product'),
    path('products/<str:id>/edit/', edit_product, name='edit_product'),
    path('products/<str:id>/delete/', delete_product, name='delete_product'),
    path('add-product-ajax',add_product_ajax, name='add_product_ajax'),
]
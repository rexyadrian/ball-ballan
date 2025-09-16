from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.show_main, name='show_main'),
    path('products/add/', views.add_product, name='add_product'),
    path('products/<int:id>/', views.show_product, name='show_product'),
    path('products/xml/', views.show_xml, name='show_xml'),
    path('products/json/', views.show_json, name='show_json'),
    path('products/xml/<int:id>/', views.show_xml_by_id, name='show_xml_by_id'),
    path('products/json/<int:id>/', views.show_json_by_id, name='show_json_by_id'),
]
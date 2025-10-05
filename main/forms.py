from django.forms import ModelForm
from main.models import Product, Store

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = [
            "name",
            "price",
            "description",
            "thumbnail",
            "category",
            "is_featured",
            "stock",
            "brand",
        ]

class StoreForm(ModelForm):
    class Meta:
        model = Store
        fields = [
            "name",
            "description",
            "address",
            "profile",
        ]
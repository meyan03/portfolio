from django import forms
from .models import Collection, Product, Customer, Order, OrderItem


class CollectionForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = ['title']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["title", "description", "price", "inventory", "collection"]


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ["first_name", "last_name", "email", "password"]


class OrderForm(forms.Form):
    model = Order
    fields = ["customer", "order_items"]


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ["order", "product", "quantity", "unit_price"]


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["customer", "payment_status"]

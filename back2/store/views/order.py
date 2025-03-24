from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from ..forms import CollectionForm, ProductForm, CustomerForm, OrderForm, OrderItemForm
from ..models import Collection, Product, Customer, Order, OrderItem


# fetch('http://yourdomain.com/collections/new/', {
#     method: 'POST',
#     headers: {
#         'Content-Type': 'application/x-www-form-urlencoded',
#     },
#     body: new URLSearchParams({
#         'title': 'New Collection',
#         'description': 'Description of the new collection'
#     })
# })

@csrf_exempt
def order_list(request):
    orders = Order.objects.all().values()
    return JsonResponse(list(orders), safe=False)


@csrf_exempt
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return JsonResponse({
        'id': order.pk,
        'customer': order.customer.pk,
        'placed_at': order.placed_at,
        'payment_status': order.payment_status
    })


@csrf_exempt
def order_create(request):
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            return JsonResponse({'id': order.pk, 'message': 'Order created successfully'})
        else:
            return JsonResponse({'errors': form.errors}, status=400)


@csrf_exempt
def order_update(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == "POST":
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            order = form.save()
            return JsonResponse({'id': order.pk, 'message': 'Order updated successfully'})
        else:
            return JsonResponse({'errors': form.errors}, status=400)


@csrf_exempt
def order_delete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.delete()
    return JsonResponse({'message': 'Order deleted successfully'})


@csrf_exempt
def orderitem_list(request):
    orderitems = OrderItem.objects.all().values()
    return JsonResponse(list(orderitems), safe=False)


@csrf_exempt
def orderitem_detail(request, pk):
    orderitem = get_object_or_404(OrderItem, pk=pk)
    return JsonResponse({
        'id': orderitem.pk,
        'order': orderitem.order.pk,
        'product': orderitem.product.pk,
        'quantity': orderitem.quantity,
        'unit_price': orderitem.unit_price
    })


@csrf_exempt
def orderitem_create(request):
    if request.method == "POST":
        form = OrderItemForm(request.POST)
        if form.is_valid():
            orderitem = form.save()
            return JsonResponse({'id': orderitem.pk, 'message': 'OrderItem created successfully'})
        else:
            return JsonResponse({'errors': form.errors}, status=400)


@csrf_exempt
def orderitem_update(request, pk):
    orderitem = get_object_or_404(OrderItem, pk=pk)
    if request.method == "POST":
        form = OrderItemForm(request.POST, instance=orderitem)
        if form.is_valid():
            orderitem = form.save()
            return JsonResponse({'id': orderitem.pk, 'message': 'OrderItem updated successfully'})
        else:
            return JsonResponse({'errors': form.errors}, status=400)


@csrf_exempt
def orderitem_delete(request, pk):
    orderitem = get_object_or_404(OrderItem, pk=pk)
    orderitem.delete()
    return JsonResponse({'message': 'OrderItem deleted successfully'})

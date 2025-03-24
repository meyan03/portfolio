from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from ..forms import CustomerForm
from ..models import Customer

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
def customer_list(request):
    customers = Customer.objects.all()
    html_content = render_to_string(
        'customer/customer_list.html', {'customers': customers})
    json_content = JsonResponse({'customers': list(customers.values())})

    response = HttpResponse(content_type='text/html')
    response.write(html_content)
    response['X-JSON'] = json_content.content.decode('utf-8')

    return response


@csrf_exempt
def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    return render(request, 'customer/customer_detail.html', {'customer': customer})


@csrf_exempt
def customer_create(request):
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save()
            return redirect('customer_detail', pk=customer.pk)
    else:
        form = CustomerForm()
    return render(request, 'customer/customer_form.html', {'form': form})


@csrf_exempt
def customer_update(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == "POST":
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            customer = form.save()
            return redirect('customer_detail', pk=customer.pk)
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'customer/customer_form.html', {'form': form})


@csrf_exempt
def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == "POST":
        customer.delete()
        return redirect('customer_list')
    return render(request, 'customer/customer_delete.html', {'customer': customer})

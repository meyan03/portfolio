from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from ..forms import ProductForm
from ..models import Product, Image

# Javascript fetch example:
# fetch('http://127.0.0.1:8000/collections/new/', {
#     method: 'POST',
#     headers: {
#         'Content-Type': 'application/x-www-form-urlencoded',
#     },
#     body: new URLSearchParams({
#         'title': 'New Collection',
#         'description': 'Description of the new collection'
#     })
# })
# Javascript axios example:
# axios.post('http://127.0.0.1:8000/collections/new/', new URLSearchParams({
#     'title': 'New Collection',
#     'description': 'Description of the new collection'
# }), {
#     headers: {
#         'Content-Type': 'application/x-www-form-urlencoded',
#     }
# })

@csrf_exempt
def create_image(request):
    if request.method == 'POST':
        image = Image.objects.create(
            product_id=request.POST.get('product_id'),
            image=request.FILES.get('image')
        )
        return JsonResponse({'id': image.id, 'product_id': image.product_id, 'image': image.image.url})


@csrf_exempt
def get_image(request, pk):
    image = get_object_or_404(Image, pk=pk)
    return JsonResponse({'id': image.id, 'product_id': image.product_id, 'image': image.image.url})


@csrf_exempt
def delete_image(request, pk):
    image = get_object_or_404(Image, pk=pk)
    image.delete()
    return JsonResponse({'status': 'deleted'})


@csrf_exempt
def product_list(request):
    products = Product.objects.all()
    html_content = render_to_string(
        'product/product_list.html', {'products': products})
    json_content = JsonResponse(
        {'products': list(products.values())})

    response = HttpResponse(content_type='text/html')
    response.write(html_content)
    response['X-JSON'] = json_content.content.decode('utf-8')

    return response


@csrf_exempt
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product/product_detail.html', {'product': product})


@csrf_exempt
def product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm()
    return render(request, 'product/product_form.html', {'form': form})


@csrf_exempt
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            product = form.save()
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)
    return render(request, 'product/product_form.html', {'form': form})


@csrf_exempt
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        product.delete()
        return redirect('product_list')
    return render(request, 'product/product_delete.html', {'product': product})

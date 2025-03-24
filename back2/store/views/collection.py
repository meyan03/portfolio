from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from ..forms import CollectionForm
from ..models import Collection

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
def collection_list(request):
    collections = Collection.objects.all()
    html_content = render_to_string(
        'collection/collection_list.html', {'collections': collections})
    json_content = JsonResponse(
        {'collections': list(collections.values())})

    response = HttpResponse(content_type='text/html')
    response.write(html_content)
    response['X-JSON'] = json_content.content.decode('utf-8')

    return response


@csrf_exempt
def collection_detail(request, pk):
    collection = get_object_or_404(Collection, pk=pk)
    return render(request, 'collection/collection_detail.html', {'collection': collection})


@csrf_exempt
def collection_create(request):
    if request.method == "POST":
        form = CollectionForm(request.POST)
        if form.is_valid():
            collection = form.save()
            return JsonResponse({'status': 'success', 'collection_id': collection.pk})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors})

    else:
        form = CollectionForm()
    return render(request, 'collection/collection_form.html', {'form': form})


@csrf_exempt
def collection_update(request, pk):
    collection = get_object_or_404(Collection, pk=pk)
    if request.method == "POST":
        form = CollectionForm(request.POST, instance=collection)
        if form.is_valid():
            collection = form.save()
            return redirect('collection_detail', pk=collection.pk)
    else:
        form = CollectionForm(instance=collection)
    return render(request, 'collection/collection_form.html', {'form': form})


@csrf_exempt
def collection_delete(request, pk):
    collection = get_object_or_404(Collection, pk=pk)
    if request.method == "POST":
        collection.delete()
        return redirect('collection_list')
    return render(request, 'collection/collection_delete.html', {'collection': collection})

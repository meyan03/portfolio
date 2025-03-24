from django.shortcuts import render


def error_404_view(request, exception):
    return render(request, '404.html', {})


def admin_home(request):
    return render(request, 'admin.html')

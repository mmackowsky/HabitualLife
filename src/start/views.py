from django.shortcuts import render


# Create your views here.
def start_view(request):
    return render(request, 'start.html')

from django.shortcuts import render


def main_view(request):
    if request.user.is_authenticated:
        return render(request, "main.html")
    else:
        return render(request, "start.html")

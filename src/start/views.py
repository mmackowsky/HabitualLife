from django.shortcuts import redirect, render


def main_view(request):
    if request.user.is_authenticated:
        return redirect("habits")
    return render(request, "start.html")

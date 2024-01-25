from django.shortcuts import redirect, render


def main_view(request):
    if request.user.is_authenticated:
        return redirect("habits")
    else:
        return render(request, "start.html")

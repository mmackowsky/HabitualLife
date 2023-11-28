from django.urls import path
from .views import start_view


urlpatterns = [
    path('', start_view, name="start"),
]

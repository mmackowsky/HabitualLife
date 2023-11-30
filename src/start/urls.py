from django.urls import path
from .views import start_view, main_view


urlpatterns = [
    path('', start_view, name="start"),
    path('main/', main_view, name='main'),
]

from django.urls import path

from .views import IndexView
from .views import DetailView
from .apps import EcommConfig


app_name = EcommConfig.name
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('<int:pk>/', DetailView.as_view(), name='product_details'),
]

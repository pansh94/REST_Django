from rest_framework.generics import ListAPIView, CreateAPIView, \
    RetrieveUpdateDestroyAPIView, GenericAPIView
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.exceptions import  ValidationError
from django.core.cache import cache
from rest_framework.response import Response

from ecomm.serializers import ProductSerializer, ProductStatSerializer
from ecomm.models import Product


class ProductPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 100


# Api view will take care of the rendering serialized data into the json format
class ProductList(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter,)
    filterset_fields = ('name',) # enable filter with specific fields
    search_fields = ('name', 'description')
    pagination_class = ProductPagination

    def get_queryset(self):
        on_sale = self.request.query_params.get('on_sale', None)
        if on_sale is None:
            return super().get_queryset()
        queryset = Product.objects.all()
        if on_sale.lower() == 'true':
            now = timezone.now()
            return queryset.filter(
                sale_start__lte=now,
                sale_end__lte=now,
            )
        return queryset


class ProductCreate(CreateAPIView):
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        try:
            price = request.data.get('price')
            if price is not None and float(price) <= 0.0:
                raise ValidationError({"Price : must be above $0."})
        except ValueError:
            raise ValidationError({"Price : a valid no. is required."})
        return super().create(request, *args, **kwargs)


class ProductRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    lookup_field = 'id'
    serializer_class = ProductSerializer

    def delete(self, request, *args, **kwargs):
        product_id = request.data.get('id')
        response = super().delete(request, *args, **kwargs)
        if response.status_code == 204:
            cache.delete('product_data_{}'.format(product_id))
        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        if response.status_code == 200:
            product = response.data
            cache.set('product_data_{}'.format(product['id']), {
                'name': product['name'],
                'description': product['description'],
                'price': product['price'],
            })
        return response


class ProductStats(GenericAPIView):
    lookup_field = 'id'
    serializer_class = ProductStatSerializer
    queryset = Product.objects.all()

    def get(self, request, format=None, id=None):
        obj = self.get_object()
        serializer = ProductStatSerializer({
            'stats': {
                '2019-01-01':[5, 10, 15],
                '2019-01-02':[20, 1, 1],
            }
        })
        return Response(serializer.data)

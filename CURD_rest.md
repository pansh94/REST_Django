# CreateAPIView
Use to create interface for create content for a model, works with serializer. You can implement some checks using exception.
Map this API to urls.py and enjoy.
```
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.exceptions import ValidationError

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
```

# DestroyAPIView
To delete product from the db.
```
from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPiView
from django.core.cache import cache

class ProductDestroy(DestroyAPiView):
    queryset = Product.objects.all()
    lookup_field = 'id'

    def delete(self, request, *args, **kwargs):
        product_id = request.data.get('id')
        response = super().delete(request, *args, **kwargs)
        if response.status_code == 204:
            cache.delete('product_data_{}'.format(product_id))# to clear the cahe after delete a product by help of id
        return response
```

# RetrieveUpdateAPIView
One URL to handle multiple HTTP method, combine update, retrieve and delete a particular view.
```
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView

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

```

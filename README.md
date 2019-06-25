# REST_Django_App
Django REST framework serializer to serialize a model.

## Serializer
```
from rest_framework import serializers

from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'name', 'description', 'price', 'sale_start', 'sale_end',
        )

    # to modify the representation override this, we added two extra customize fields
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['is_on_sale'] = instance.is_on_sale()
        data['current_price'] = instance.current_price()
        return data
------------------------------------------------------------------------------------
from .models import Product
from .serializer import ProductSerializer

from rest_framework.renderers import JSONRenderer


product = Product.objects.all()[0]
serializer = ProductSerializer()
data = serializer.to_representation(product)
renderer = JSONRenderer()
renderer.render(data) #to render data in JSON
```

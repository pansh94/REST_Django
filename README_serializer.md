# REST_Django_App
Django REST framework serializer to serialize a model.

## Serializer
Serialization/Deserialixation is done to convert obj into it's JSON representation before sending to user and parse the incoming JSON etc data into obj before saving into db.
```
#add rest_framework in settings.py
INSTALLED_APPS = (
    ...
    'rest_framework',
    'snippets.apps.SnippetsConfig',
)
--------------------------------------------------------------------------------
from rest_framework import serializers
from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES


class SnippetSerializer(serializers.Serializer):
    #data to be serialized or deserialized
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=False, allow_blank=True, max_length=100)
    code = serializers.CharField(style={'base_template': 'textarea.html'})
    linenos = serializers.BooleanField(required=False)
    language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
    style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Snippet.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.code = validated_data.get('code', instance.code)
        instance.linenos = validated_data.get('linenos', instance.linenos)
        instance.language = validated_data.get('language', instance.language)
        instance.style = validated_data.get('style', instance.style)
        instance.save()
        return instance
```
serialization 
```
serializer = SnippetSerializer(snippet)
serializer.data
# {'id': 2, 'title': '', 'code': 'print("hello, world")\n', 'linenos': False, 'language': 'python', 'style': 'friendly'}
content = JSONRenderer().render(serializer.data)
content
# b'{"id": 2, "title": "", "code": "print(\\"hello, world\\")\\n", "linenos": false, "language": "python", "style": "friendly"}'
```
Deserialization is similar. First we parse a stream into Python native datatypes...
```
import io

stream = io.BytesIO(content)
data = JSONParser().parse(stream)
```
...then we restore those native datatypes into a fully populated object instance.
```
serializer = SnippetSerializer(data=data)
serializer.is_valid()
# True
serializer.validated_data
# OrderedDict([('title', ''), ('code', 'print("hello, world")\n'), ('linenos', False), ('language', 'python'), ('style', 'friendly')])
serializer.save()
# <Snippet: Snippet object>
```
We can also serialize querysets instead of model instances. To do so we simply add a many=True flag to the serializer arguments.
```
serializer = SnippetSerializer(Snippet.objects.all(), many=True)
serializer.data
```
# Using ModelSerializer
```
--------------------------------------------------------------------------------
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
########################################################################
class SnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snippet
        fields = ('id', 'title', 'code', 'linenos', 'language', 'style')
```
It's important to remember that ModelSerializer classes don't do anything particularly magical, they are simply a shortcut for creating serializer classes:
1. An automatically determined set of fields.
2. Simple default implementations for the create() and update() methods.

# Simplifying Serialization
Serializing using field
```
class ProductSerializer(serializers.ModelSerializer):
    # read_only decide wheather or not we can serialize using serializer
    is_on_sale = serializers.BooleanField(read_only=True)
    current_price = serializers.FloatField(read_only=True)
    description = serializers.CharField(min_length=2, max_length=200)# this will ensure validation

    class Meta:
        model = Product
        fields = (
            'id','name', 'description', 'price', 'sale_start', 'sale_end',
            'current_price','is_on_sale',
        )
```

# SerializeMethodField
get_ is prefix to the field name for the method that is called. You can serialize of one or many item using many parameter.
many = True (create a list of serialize of model instance)
many = False (will serialize only one model instance)
```
class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingCartItem
        fields = (
            'product', 'quantity',
        )


class ProductSerializer(serializers.ModelSerializer):
    # read_only decide wheather or not we can serialize using serializer
    is_on_sale = serializers.BooleanField(read_only=True)
    current_price = serializers.FloatField(read_only=True)
    description = serializers.CharField(min_length=2, max_length=200)# this will ensure validation
    cart_items = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            'id','name', 'description', 'price', 'sale_start', 'sale_end',
            'current_price','is_on_sale', 'cart_items',
        )

    def get_cart_items(self, instance):
        items = ShoppingCartItem.obejects.filter(product=instance)
        return CartItemSerializer(items, many=True).data
------------------------------------------------------------------------------
import json
>>> from ecomm.models import *
>>> from ecomm.serializers import *
>>> p = Product.objects.all().first()
>>> c = ShoppingCart()
>>> c.save()
>>> i = ShoppingCartItem(product=p,shopping_cart=c,quantity=3)
>>> i.save()
>>> ser = ProductSerializer(p)
>>> print(json.dumps(ser.data, indent=2))
```
# NumberFeild With Serializer
1. IntegerField
```
quantity = serializer.IntegerField(min_value=1 , max_value=100)
```
2. FloatField
```
price = serializer.FloatField(min_value=1.0, max_value=100000)
```
3. DecimalField
more powerful than FloatField with max_digits and decimal_places.
```
price = serializer.DecimalField(min_value=1.00, max_value=100000, max_digits=None, decimal_places=2)
```

# Date and Time field with serializer
1. input_formats : format
2. format : format
3. help_text : Appear in broeser for REST API.
4. style : control how field appear in REST API
```
sale_start = serializers.DateTimeField(
    input_formats=['%I:%M %p %d %B %Y'], format=None, allow_null=True,
    help_text='Accepted format is "12:03 PM 16 April 2018"',
    style={'input_type':'text', 'placeholder':'12:03 PM 16 July 2020'},
)
```

# Plain Serializer
```
class ProductStatSerializer(serializers.Serializer):
    stats = serializers.DictField(
        child=serializers.ListField(
            child=serializers.IntegerField(),
        )
    )
```
# Serilize with ImageField and FileField
FileField has write_only and read_only field attribute. validated_data attribute is data that passed through serializer and moodel validate process. It is used to create and update model.
```
    photo = serializers.ImageField(default=None)
    warranty = serializers.FileField(write_only=True, default=None)

    def update(self, instance, validated_data):
        if validated_data.get('warranty'):
            instance.description += '\n\nWarranty\n\n'
            instance.description += b'; '.join(
                validated_data['warranty'].readlines()
            ).decode()
        return instance
```

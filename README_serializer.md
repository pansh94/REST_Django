# REST_Django_App
Django REST framework serializer to serialize a model.

## Serializer
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

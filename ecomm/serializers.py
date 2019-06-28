from rest_framework import serializers

from .models import Product, ShoppingCartItem


class CartItemSerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField(max_value=100, min_value=1)

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
    price = serializers.DecimalField(
        min_value=1.00, max_value=100000,
        max_digits=None, decimal_places=2,
    )
    sale_start = serializers.DateTimeField(
        required=False,
        input_formats=['%I:%M %p %d %B %Y'], format=None, allow_null=True,
        help_text='Accepted format is "12:03 PM 16 April 2018"',
        style={'input_type': 'text', 'placeholder': '12:03 PM 16 July 2020'},
    )
    sale_end = serializers.DateTimeField(
        required=False,
        input_formats=['%I:%M %p %d %B %Y'], format=None, allow_null=True,
        help_text='Accepted format is "12:03 PM 16 April 2018"',
        style={'input_type':'text', 'placeholder':'12:03 PM 16 July 2020'},
    )
    photo = serializers.ImageField(default=None)
    warranty = serializers.FileField(write_only=True, default=None)

    class Meta:
        model = Product
        fields = (
            'id','name', 'description', 'price', 'sale_start', 'sale_end',
            'current_price','is_on_sale', 'cart_items',
            'photo', 'warranty',
        )

    def get_cart_items(self, instance):
        items = ShoppingCartItem.objects.filter(product=instance)
        return CartItemSerializer(items, many=True).data

    def update(self, instance, validated_data):
        if validated_data.get('warranty'):
            instance.description += '\n\nWarranty\n\n'
            instance.description += b'; '.join(
                validated_data['warranty'].readlines()
            ).decode()
        return super().update(instance, validated_data)

    def create(self, validated_data):
        validated_data.pop('warranty')
        return Product.objects.create(**validated_data)


class ProductStatSerializer(serializers.Serializer):
    stats = serializers.DictField(
        child=serializers.ListField(
            child=serializers.IntegerField(),
        )
    )

from rest_framework.test import APITestCase
import os.path
from django.conf import settings

from ecomm.models import Product


class ProductTestCase(APITestCase):
    def test_create_product(self):
        initial_product_count = Product.objects.count()
        product_attrs = {
            'name': 'New Product',
            'description': 'Awesome product',
            'price': '123.45',
        }
        response = self.client.post(
            '/api/v1/products/new',
            product_attrs,
        )

        if response.status_code != 201:
            print(response.data)

        self.assertEqual(
            Product.objects.count(),
            initial_product_count+1,
        )

        for attr, expected_value in product_attrs.items():
            self.assertEqual(
                response.data[attr],
                expected_value,
            )

        self.assertEqual(
            response.data['is_on_sale'],
            False,
        )
        self.assertEqual(
            response.data['current_price'],
            float(product_attrs['price']),
        )

class ProductDestroyTestCase(APITestCase):
    def test_product_delete(self):
        Product.objects.create(
            name='New Product',
            description='Awesome product',
            price='123.45',
        )
        initial_product_count = Product.objects.count()
        product_id = Product.objects.all().first().id
        self.client.delete(
            '/api/v1/products/{}/'.format(product_id)
        )
        self.assertEqual(
            initial_product_count-1,
            Product.objects.count(),
        )
        self.assertRaises(
            Product.DoesNotExist,
            Product.objects.get, id=product_id,
        )


class ProductListTestCase(APITestCase):
    def test_product_list(self):
        Product.objects.create(
            name='New Product',
            description='Awesome product',
            price='123.45',
        )
        products_count = Product.objects.count()
        response = self.client.get('/api/v1/products')
        self.assertIsNone(response.data['next'])
        self.assertIsNone(response.data['previous'])
        self.assertEqual(response.data['count'], products_count)
        self.assertEqual(len(response.data['results']), products_count)


class ProductUpdateTest(APITestCase):
    def test_update_product(self):
        Product.objects.create(
            name='Test Product',
            description='Test product',
            price='123.45',
        )
        product = Product.objects.first()
        response = self.client.patch(
            '/api/v1/products/{}/'.format(product.id),
            {
                'name': 'New Product',
                'description': 'Awesome Product',
                'price': 20.00
            },
            format='json',
        )
        updated = Product.objects.get(id=product.id)
        self.assertEqual(updated.name,'New Product')
        self.assertEqual(updated.description, 'Awesome Product')
        self.assertEqual(updated.price,20.00)

    def test_upload_product_photo(self):
        Product.objects.create(
            name='Test Product',
            description='Test product',
            price='123.45',
        )
        product = Product.objects.first()
        original_photo = product.photo
        photo_path = os.path.join(
            settings.MEDIA_ROOT, 'products', 'v_c.jpg'
        )
        with open(photo_path, 'rb') as photo_data:
            response = self.client.patch(
                '/api/v1/products/{}/'.format(product.id),
                { 'photo': photo_data },
                format='multipart',
            )
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.data['photo'],original_photo)

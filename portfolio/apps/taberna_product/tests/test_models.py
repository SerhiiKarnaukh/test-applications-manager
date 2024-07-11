from django.test import TestCase
from accounts.models import Account

from taberna_product.models import Category, Product


class TestCategoriesModel(TestCase):

    def setUp(self):
        self.data1 = Category.objects.create(name='django', slug='django')

    def test_category_model_entry(self):
        """
        Test Category model data insertion/types/field attributes
        """
        data = self.data1
        self.assertTrue(isinstance(data, Category))
        self.assertEqual(str(data), 'django')


#     def test_category_url(self):
#         """
#         Test category model slug and URL reverse
#         """
#         data = self.data1
#         response = self.client.post(
#             reverse('store:category_list', args=[data.slug]))
#         self.assertEqual(response.status_code, 200)


class TestProductsModel(TestCase):

    def setUp(self):
        Category.objects.create(name='django', slug='django')
        Account.objects.create(username='admin')
        self.data1 = Product.objects.create(category=1,
                                            created_by_id=1,
                                            name='django advanced',
                                            slug='django advanced',
                                            price='20.00',
                                            image='django',
                                            stock=0)

    def test_products_model_entry(self):
        """
        Test product model data insertion/types/field attributes
        """
        data = self.data1
        self.assertTrue(isinstance(data, Product))
        self.assertEqual(str(data), 'django beginners')


#     def test_products_url(self):
#         """
#         Test product model slug and URL reverse
#         """
#         data = self.data1
#         url = reverse('store:product_detail', args=[data.slug])
#         self.assertEqual(url, '/item/django-beginners/')
#         response = self.client.post(
#             reverse('store:product_detail', args=[data.slug]))
#         self.assertEqual(response.status_code, 200)

#     def test_products_custom_manager_basic(self):
#         """
#         Test product model custom manager returns only active products
#         """
#         data = Product.products.all()
#         self.assertEqual(data.count(), 1)

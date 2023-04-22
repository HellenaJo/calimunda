import django_filters
from .models import Category,Product

'''
create class in filters to filter models eg Product
class Meta in django; alters/manipulates content of another class
fields; specifify many thinggs from thre rg issuedQuantity, totalQuantity
we use filter when going to include the search functionality
'''

class Product_filter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = ['itemName']

class Category_filter(django_filters.FilterSet):
    class Meta:
        model = Category
        fields = ['name']
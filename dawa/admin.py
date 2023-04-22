from django.contrib import admin
from .models import *    # *; means all

# Register your models here.
admin.site.register(Category)
admin.site.register(Product)

'''
the asmin is he only one  who can input stock in inventory and others sale but he is also given
acess to make sales
''' 
admin.site.register(Sale)
admin.site.register(Payment)

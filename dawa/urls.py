from django.urls import path
from dawa import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('index/', views.index, name = 'index'),
    path('home/', views.index, name = 'home'),
    path('', auth_views.LoginView.as_view(template_name = 'products/login.html'), name = 'login'),
    path('logout/', auth_views.LogoutView.as_view(template_name = 'products/logout.html'), name = 'logout'),
    #this is a buying button route for all products
    path('index/<int:product_id>/', views.product_detail, name = 'product_detail'),
    path('issue_item/<str:pk>/', views.issue_item, name = 'issue_item'),
    path('add_to_stock/<str:pk>/', views.add_to_stock, name = 'add_to_stock'), 
    #handles receipt after a sucessful sale
    path('receipt/', views.receipt, name ='receipt'),
    #handling all sales request from the web browser
    path('all_sales/', views.all_sales, name = 'all_sales'),
    path('receipt/<int:receipt_id>/', views.receipt_detail, name = 'receipt_detail'),
    path('', views.initiate_payment, name='initiate_payment'),
    path('str:ref>/', views.verify_payment, name ='verify_payment'),
]

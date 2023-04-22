from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product,Sale,Payment
#we include the filters to used by views through import
from .filters import Product_filter
#we are including our models form ceated in the models file
from .forms import AddForm,SaleForm
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from dawa import forms
from django.conf import settings
from django.contrib import messages
# Create your views here.
'''

views; gets data from the database and forwards it to the requested page
we let view know about the models.file so that it can use that data
'''
def index(request):
    products = Product.objects.all().order_by('-id')
    #queryset; uses products filtered by their ids
    product_filters = Product_filter(request.GET,queryset= products) 
    products = product_filters.qs
    return render(request, 'products/index.html', {'products':products, 'product_filters':product_filters})

#this home loads the index page
@login_required
def home(request):
    return render(request, 'products/aboutdrcali.html')

#view for product_detail
#login required iss fuction that works on a login request to return view ie fisrdt login and aceess the view
@login_required
def product_detail(request, product_id):
    product = Product.objects.get(id = product_id)
    return render(request, 'products/product_detail.html', {'product':product})

@login_required
def issue_item(request, pk):
    issued_item = Product.objects.get(id = pk)
    sales_form = SaleForm(request.POST) #post comes as a reuest from the form
    '''
    we receive post from browser and form is also valid(has valid values based on prescripton 
    from model) then proceed
    '''
    if request.method == 'POST':
        if sales_form.is_valid():
#if everything is correct, we save the data in the corresponding model
#commit is a boolean(false) which saves form once for evry instance called and true commit just duplicates dats
            new_sale = sales_form.save(commit = False)
            new_sale.item = issued_item #GETS ID OF issue_item
            new_sale.unitPrice = issued_item.unitPrice
            new_sale.save()
            #we are going to keep track of stosck remaining after sales
            issuedQuantity = int(request.POST['quantity'])
            issued_item.totalQuantity -= issuedQuantity
            issued_item.save()
            print(issued_item.itemName)
            print(request.POST['quantity'])
            print(issued_item.totalQuantity)

            return redirect('receipt')
    return render(request, 'products/issue_item.html', {'sales_form':sales_form})

@login_required
def receipt(request):
    sales = Sale.objects.all().order_by('-id')
    return render(request, 'products/receipt.html', {'sales':sales})

@login_required
def add_to_stock(request, pk):
    issued_item = Product.objects.get(id =pk)
    form = AddForm(request.POST)
    if request.method == 'POST':
        #nested if
        #if data in form is confirmed valid 
        if form.is_valid():
            add_quantity = int(request.POST['receivedQuantity'])
            issued_item.totalQuantity += add_quantity
            issued_item.save()
            #to add to the remaining stock that qtty is reducing as u buy
            print(add_quantity)
            print(issued_item.totalQuantity)
            return redirect('home')
    return render(request, 'products/add_to_stock.html', {'form':form})  #{} r 4 dictionary

@login_required
def all_sales(request):
    sales = Sale.objects.all()
    total = sum([items.amountReceived for items in sales])
    change = sum([items.getChange() for items in sales])
    net = total - change
    return render(request, 'products/all_sales.html', {
        'sales': sales,
        'total': total,
        'change': change,
        'net': net,
    })

@login_required
def receipt_detail(request, receipt_id):
    receipt = Sale.objects.get(id = receipt_id)
    return render(request, 'products/receipt_detail.html', {'receipt': receipt})

#USERS TO INISATE PAYMENT
#call payment function to generate a ref to make payenst
@login_required
def initiate_payment(request: HttpResponse) -> HttpResponse:
    if request.method == "POST":
        payment_form  = forms.PaymentForm(request.POST)
        if payment_form.is_valid():
            payment = payment_form.save()
            return render(request, 'products/make_payment.html', {'payment':payment, 'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY})
   
    
def verify_payment(request: HttpRequest, ref: str) -> HttpResponse:
    payment = get_object_or_404(Payment, ref=ref)
    verified = payment.verify_payment()
    if verified:
        messages.success(request, 'Verification Successful')
    else:
        messages.error(request, 'Verification Failed')
        payment_form = forms.PapmentForm()
        return render(request, 'products/initiate_payment.html', {'payment_form':payment_form})


    

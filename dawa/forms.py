#creates form file which gets its base or links to from the templates and models
#this is a user inerface for entering data
from django.forms import ModelForm

#accessing  our models so that we link them to forms
from .models import *

#forms to be used by others cz the ones before were used by admin only
class AddForm(ModelForm):
    class Meta:
        model = Product   #updates product
#updates amount stock ie stock added on the current stock
        fields = ['receivedQuantity']  
     
#we modelling a form basing on our model that we shall use to record a product sale
class SaleForm(ModelForm):
#class meta is usd to acess and manipulate a model
    class Meta:
        model = Sale
        fields = ['quantity', 'amountReceived', 'issuedTo']

class PaymentForm(ModelForm):
    class Meta:
        model = Payment
        fields = ['amount']
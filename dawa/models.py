from django.db import models
import secrets
from .paystack import PayStack

# Create your models here.
'''
models.py;is physical space on the database where we are going to store data about things
models; spaces on the database where we store things
view; py function connected to the model
model; acts as a 3rd party where we can store btn the server,client and database
class eg Category shd always be singular
after creating model, we make migrations 
  makemigrations:creates file to keep track o the model ie python manage.py makemigrations
  migrate:creates a physical database space ie python manage.py migrate
EVERY TIME U CHANGE SH IN THE MODEL, U HV TO MIGRATE
BEFORE MAKING MIGRATION,STOP SERVER. 
THEN AFTER MAKING MIGRATIONS, START SERVER
'''

'''
__str__ mtd; specifies how the object shd be called by other objects ie the human readable name
every model shd hv a name
name in models is a field/memory int he database not a variable
null; value unknown
blank; value is empty
max_length; cant go beyond 50 xters
charfield; xters field
'''

class Category(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True) 
    def __str__(self):
        return self.name

'''
foreignkey; connects category and product and creates a relationship between tables
its a primary key thats is automaticlly assigned to the foreignkey
on_delete: means if a model(category) is deleted, everything is lost


'''
class Product(models.Model):
    categoryName = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    itemName = models.CharField(max_length=50, null=True, blank=True)
    totalQuantity = models.IntegerField(default=0, null=True, blank=True)
    issuedQuantity = models.IntegerField(default=0, null=True, blank=True)
    receivedQuantity = models.IntegerField(default=0, null=True, blank=True)
    unitPrice = models.IntegerField(default=0, null=True, blank=True)
    manufacturer = models.CharField(max_length=50, null=True, blank=True)
    brand = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.itemName

class Sale(models.Model):
    #hv to add more things here of my own
    #IF WE DELETE PRODUCT, EVERYTHING CONCERNING PRODUCT WILL DISAPPEAR(CASCADE)
    item = models.ForeignKey(Product, on_delete = models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    amountReceived = models.IntegerField(default=0, null=True, blank=True)
    unitPrice = models.IntegerField(default=0, null=True, blank=True)
    issuedTo = models.CharField(max_length=50, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

#this method calculates the total sale
    def getTotal(self):
        total = self.quantity * self.item.unitPrice
        return int(total)
    
#this method calculates the change
#abs is absolute ie it records the whole number not decimals
    def getChange(self):
        change = self.getTotal() - self.amountReceived
        return abs(int(change))

#THIS IS THE SHISHI MTD    
#item.itemName; means we are accessing the name via ts sale ie tha t the sale has been bought
    def __str__(self):
        return self.item.itemName
    
    def getVat(self):
        pass

#mtd get vat
#total - vat(18%)
#cashiernm, vat, buyername,da

class Payment(models.Model):
    amount = models.PositiveIntegerField()
    ref = models.CharField(max_length=200)
    email = models.EmailField()
    verified = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

class Meta:
    ordering = ('-date',)

    def __str__(self) -> str:
       return f"Payment: {self.amount}"

#check if object has a unique reference and if t doesnt we create one using secrets model wc generates APIs
    def save(self, *args, **kwargs) -> None:
        while not self.ref:
            ref = secrets.token_urlsafe(50) #secrets model
            objects_with_similar_ref = Payment.objects.filter(ref=ref)
            if not objects_with_similar_ref:
                self.ref = ref
        super().save(*args, **kwargs)

    def amount_value(self) -> int:
       return self.amount *100

    def verify_payment(self):
        paystack = PayStack()   
        status, result = paystack.verify_payment(self.ref, self.amount)            
        if status:
            if result['amount'] / 100 == self.amount:
                self.verified = True
            self.save()
        if self.verified:
            return True
        return False

    
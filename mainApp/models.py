from django.db import models
from django.db import models

class MainCategory(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=30)
    def __str__(self):
        return str(self.id)+' '+self.name

class SubCategory(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=30)
    def __str__(self):
        return str(self.id)+' '+self.name

class Brand(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=30)
    def __str__(self):
        return str(self.id)+' '+self.name

class Seller(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=30)
    username=models.CharField(max_length=20)
    mobile_no=models.CharField(max_length=20)
    email=models.CharField(max_length=30)
    address1=models.CharField(max_length=20,blank=True,null=True,default=None)
    address2=models.CharField(max_length=20,blank=True,null=True,default=None)
    address3=models.CharField(max_length=20,blank=True,null=True,default=None)
    city=models.CharField(max_length=20,blank=True,null=True,default=None)
    otp=models.IntegerField(default=0)
    state=models.CharField(max_length=20,blank=True,null=True,default=None)
    pin=models.CharField(max_length=10,blank=True,null=True,default=None)
    pic=models.ImageField(upload_to="images/",blank=True,null=True,default=None)
    def __str__(self):
        return str(self.id)+' '+self.name

class Product(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=30)
    maincat=models.ForeignKey(MainCategory,on_delete=models.CASCADE)
    subcat=models.ForeignKey(SubCategory,on_delete=models.CASCADE)
    brand=models.ForeignKey(Brand,on_delete=models.CASCADE)
    seller=models.ForeignKey(Seller,on_delete=models.CASCADE,default=1)
    baseprice=models.IntegerField()
    discount=models.IntegerField(default=0) 
    finalprice=models.IntegerField()
    color=models.CharField(max_length=30)
    size=models.CharField(max_length=30)
    description=models.TextField(default=None)
    stock=models.BooleanField(default=True)
    time=models.DateTimeField(auto_now=True)
    pic1=models.ImageField(upload_to="images/",blank=True,null=True,default=None)
    pic2=models.ImageField(upload_to="images/",blank=True,null=True,default=None)
    pic3=models.ImageField(upload_to="images/",blank=True,null=True,default=None)
    pic4=models.ImageField(upload_to="images/",blank=True,null=True,default=None) 
    def __str__(self):
        return str(self.id)+' '+self.name

class Buyer(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=30)
    username=models.CharField(max_length=20)
    mobile_no=models.CharField(max_length=20)
    email=models.CharField(max_length=30)
    address1=models.CharField(max_length=20,blank=True,null=True,default=None)
    address2=models.CharField(max_length=20,blank=True,null=True,default=None)
    address3=models.CharField(max_length=20,blank=True,null=True,default=None)
    city=models.CharField(max_length=20,blank=True,null=True,default=None)
    state=models.CharField(max_length=20,blank=True,null=True,default=None)
    otp=models.IntegerField(default=0)
    pin=models.CharField(max_length=10,blank=True,null=True,default=None)
    pic=models.ImageField(upload_to="images/",blank=True,null=True,default=None)
    def __str__(self):
        return str(self.id)+' '+self.name

class Wishlist(models.Model):
    id=models.AutoField(primary_key=True)
    buyer=models.ForeignKey(Buyer,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    def __str__(self):
        return str(self.id)+' '+self.buyer+' '+self.product

choice = ((1,"Not Packed"),(2,"Packed"),(3,"Out for Delivery"),(4,"Delivered"))
paymentChoice = ((1,"Pending"),(2,"Done"))
mode = ((1,"COD"),(2,"Net Banking"))
class Checkout(models.Model):
    id = models.AutoField(primary_key=True)
    buyer = models.ForeignKey(Buyer,on_delete=models.CASCADE)
    products = models.CharField(max_length=20)
    total = models.IntegerField()
    shipping = models.IntegerField(default=0)
    finalAmount = models.IntegerField()
    status = models.IntegerField(choices=choice,default=1)
    paymentStatus = models.IntegerField(choices=paymentChoice,default=1)
    mode = models.IntegerField(choices=mode,default=1)
    time = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    orderId = models.CharField(max_length=50,default=None,blank=True,null=True)
    paymentId = models.CharField(max_length=50,default=None,blank=True,null=True)
    paymentsignature = models.CharField(max_length=50,default=None,blank=True,null=True)

    def __str__(self):
        return str(self.id)+" "+self.buyer.username+" "+str(self.active)

class Subscribe(models.Model):
    id=models.AutoField(primary_key=True)
    email=models.CharField(max_length=30)
    def __str__(self):
        return str(self.id)+' '+self.email

class Contact(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=30)
    email=models.CharField(max_length=30)
    subject=models.CharField(max_length=20)
    message=models.TextField()
    mobile=models.CharField(max_length=12,default='',null=True)
    active=models.BooleanField(default=True)
    
    def __str__(self):
        return str(self.id)+' '+self.name+' '+self.subject+' '+str(self.active)


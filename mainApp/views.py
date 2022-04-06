from email import message
from django.shortcuts import render,HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import auth,messages
from django.contrib.auth.decorators import login_required
from .models import *
from OnlineShop.settings import RAZORPAY_API_KEY,RAZORPAY_API_SECRET_KEY
import razorpay
from django.conf import settings
from django.core.mail import send_mail
import random

def home(request):
    data=Product.objects.all()
    data=data[::-1]
    return render(request,'home.html',{'Data':data})
def shop(request,mc,sc,br):
    maincat=MainCategory.objects.all()
    subcat=SubCategory.objects.all()
    brand=Brand.objects.all()
    if(mc=='all' and sc=='all' and br=='all'):       
        data=Product.objects.all()
    elif(mc!='all' and sc=='all' and br=='all'):
        data=Product.objects.filter(maincat=MainCategory.objects.get(name=mc))
    elif(mc=='all' and sc!='all' and br=='all'):
        data=Product.objects.filter(subcat=SubCategory.objects.get(name=sc))
    elif(mc=='all' and sc=='all' and br!='all'):
        data=Product.objects.filter(brand=Brand.objects.get(name=br))
    elif(mc!='all' and sc!='all' and br=='all'):
        data=Product.objects.filter(maincat=MainCategory.objects.get(name=mc),subcat=SubCategory.objects.get(name=sc))
    elif(mc!='all' and sc=='all' and br!='all'):
        data=Product.objects.filter(maincat=MainCategory.objects.get(name=mc),brand=Brand.objects.get(name=br))
    elif(mc=='all' and sc!='all' and br!='all'):
        data=Product.objects.filter(subcat=SubCategory.objects.get(name=sc),brand=Brand.objects.get(name=br))
    elif(mc!='all' and sc!='all' and br!='all'):
        data=Product.objects.filter(maincat=MainCategory.objects.get(name=mc),subcat=SubCategory.objects.get(name=sc),brand=Brand.objects.get(name=br))

    return render(request,'shop.html',{'maincat':maincat,
                                        'subcat':subcat,
                                        'brand':brand,
                                        'Data':data,
                                        'MC':mc,
                                        'SC':sc,
                                        'BR':br})
def productsection(request,id):
    data=Product.objects.get(id=id)
    if(request.method=="POST"):
        try:
            buyer=Buyer.objects.get(username=request.user)
        except:
            return HttpResponseRedirect('/sellerprofile/')
        cart=request.session.get('cart',None)
        quantity=int(request.POST.get('quantity'))
        if(cart):
            if(str(id) in cart.keys()):
                cart[str(id)]+=int(quantity)
            else:
                cart.setdefault(str(id),int(quantity))
        else:
            cart={str(data.id):quantity}
        request.session['cart']=cart
        return HttpResponseRedirect('/cart/')
    return render(request,'productsection.html',{'Data':data})
@login_required(login_url='/login/')
def cart(request):
    sum=0
    dis=0
    try:
        buyer=Buyer.objects.get(username=request.user)
    except:
        return HttpResponseRedirect('/sellerprofile/')
    flushcart = request.session.get("flushcart",None)
    if(flushcart==True):
        request.session['cart']={}
        request.session['flushcart']=False
    cart=request.session.get('cart')
    product=[] 
    if(cart):
        for i,j in cart.items():
            p=Product.objects.get(id=i)
            product.append(p)
            sum=sum+p.baseprice*int(j)
            dis=dis+p.discount*int(j)*p.baseprice/100
    total=int(sum)-int(dis)
    data={'sum':sum,'dis':dis,'total':total}
    if(request.method=='POST'):
        id=request.POST.get('id')
        q=request.POST.get('quantity')
        cart[id]=q
        request.session['cart']=cart
        request.session.set_expiry(60*60*24*30)   
    return render(request,'cart.html',{'Product':product,'Data':data})
@login_required(login_url='/login/')
def deletecart(request,id):
    try:
        cart=request.session.get('cart')
        cart.pop(str(id))
        request.session['cart']=cart
    except:
        return HttpResponseRedirect('/cart/')
    return HttpResponseRedirect('/cart/')
def login(request):
    if(request.method=="POST"):
        username=request.POST.get("username")
        password=request.POST.get("password")
        user=auth.authenticate(username=username,password=password)
        if(user is not None):
            auth.login(request,user)
            if(user.is_superuser):
                return HttpResponseRedirect('/admin/')
            else:
                return HttpResponseRedirect('/')
        else:
            messages.error(request,"Please Enter valid Details!!")
    return render(request,'login.html')
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')
def signup(request):
    if(request.method=='POST'):
        actype=request.POST.get('actype')
        if(actype=='seller'):
           s=Seller()
           s.name=request.POST.get('name')
           s.username=request.POST.get('username')
           s.mobile_no=request.POST.get('mobile')
           s.email=request.POST.get('email')
           pswd=request.POST.get('password')
           try:
                user=User.objects.create_user(username=s.username,password=pswd)
                user.save() 
                s.save()
           except:
                messages.error(request,"UserName Already exist!")
                return HttpResponseRedirect('/signup/')
        elif(actype=='buyer'):
           b=Buyer()
           b.name=request.POST.get('name')
           b.username=request.POST.get('username')
           b.mobile_no=request.POST.get('mobile')
           b.email=request.POST.get('email')
           pswd=request.POST.get('password')
           try:
                user=User.objects.create_user(username=b.username,password=pswd)
                user.save()
                b.save()
           except:
                messages.error(request,"UserName Already exist!")
                return HttpResponseRedirect('/signup/')         
        return HttpResponseRedirect('/login/')
    return render(request,'signup.html')

@login_required(login_url='/login/')
def profile(request):#----------Seller profile
    try:
        data=Seller.objects.get(username=request.user)
        products=Product.objects.filter(seller=data)
        return render(request,'sellerprofile.html',{'Data':data,'Product1':products})
    except:
        return HttpResponseRedirect('/buyerprofile/')

@login_required(login_url='/login/')
def buyerprofile(request):#---------Buyer's Profile
    try:
        buyer=Buyer.objects.get(username=request.user)
    except:
        return HttpResponseRedirect('/')
    wishlist=Wishlist.objects.filter(buyer=buyer)
    check=Checkout.objects.filter(buyer=buyer)
    return render(request,'buyerprofile.html',{'Data':buyer,'Wishlist':wishlist,'Checkout':check})

@login_required(login_url='/login/')
def updataprofile(request):#---------seller profile updating
    try:
        data=Seller.objects.get(username=request.user)
    except:
        data=Buyer.objects.get(username=request.user)
    if(request.method=="POST"):
        data.name=request.POST.get('name')
        data.email=request.POST.get('email')
        data.mobile_no=request.POST.get('mobile')
        data.address1=request.POST.get('add1')
        data.address2=request.POST.get('add2')
        data.address3=request.POST.get('add3')
        data.state=request.POST.get('state')
        data.city=request.POST.get('city')
        data.pin=request.POST.get('pin')
        if(request.FILES.get('pic')):
            data.pic=request.FILES.get('pic')
        data.save()
        messages.error(request,'Your Profile Updated')
        return HttpResponseRedirect('/updateprofile/')
    return render(request,'updateprofile.html',{"Data":data})

@login_required(login_url='/login/')
def AddProduct(request):
    data=Brand.objects.all()
    data1=MainCategory.objects.all()
    data2=SubCategory.objects.all()
    if(request.method=="POST"):
        p=Product()
        p.name=request.POST.get('name')
        p.brand=Brand.objects.get(name=request.POST.get('brand'))
        p.maincat=MainCategory.objects.get(name=request.POST.get('maincategory'))
        p.subcat=SubCategory.objects.get(name=request.POST.get('subcategory'))
        p.stock=request.POST.get('stock')
        p.baseprice=int(request.POST.get('baseprice'))
        p.discount=int(request.POST.get('discount'))
        p.finalprice=p.baseprice-p.baseprice*p.discount/100
        p.color=request.POST.get('color')
        p.size=request.POST.get('size')
        p.description=request.POST.get('description')
        p.seller=Seller.objects.get(username=request.user)
        if(request.FILES.get('pic1')):
            p.pic1=request.FILES.get('pic1')
        if(request.FILES.get('pic2')):
            p.pic2=request.FILES.get('pic2')
        if(request.FILES.get('pic3')):
            p.pic3=request.FILES.get('pic3')
        if(request.FILES.get('pic4')):
            p.pic4=request.FILES.get('pic4')
        p.save()
        email=Subscribe.objects.all()
        for i in email:
            subject = 'welcome to ONLINESHOP world'
            message = f'Hi, We have Added a new Product {p.name} please check it out.'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [i.email, ]
            send_mail( subject, message, email_from, recipient_list )
        return HttpResponseRedirect('/sellerprofile/')
    return render(request,'AddProduct.html',{"Data":data,"Data1":data1,"Data2":data2})

@login_required(login_url='/login/')
def editproduct(request,id):
    #seller=Seller.objects.get(username=request.user)
    product=Product.objects.get(id=id)
    maincat=MainCategory.objects.all()
    subcat=SubCategory.objects.all()
    brand=Brand.objects.all()
    if(request.method=="POST"):
        product.name=request.POST.get('name')
        product.brand=Brand.objects.get(name=request.POST.get('brand'))
        product.subcat=SubCategory.objects.get(name= request.POST.get('subcategory'))
        product.maincat=MainCategory.objects.get(name=request.POST.get('maincategory'))
        product.baseprice=int(request.POST.get('baseprice'))
        product.discount=int(request.POST.get('discount'))
        product.finalprice=product.baseprice-product.baseprice*product.discount/100
        product.description=request.POST.get('description')
        product.size=request.POST.get('size')
        product.color=request.POST.get('color')
        product.stock=request.POST.get('stock')
        if(request.FILES.get('pic1')):
            product.pic1=request.FILES.get('pic1')
        if(request.FILES.get('pic2')):
            product.pic2=request.FILES.get('pic2')
        if(request.FILES.get('pic3')):
            product.pic3=request.FILES.get('pic3')
        if(request.FILES.get('pic4')):
            product.pic4=request.FILES.get('pic4')
        product.save()
        return HttpResponseRedirect("/sellerprofile/")
    return render(request,'EditProduct.html',{'Product':product,'maincat':maincat,
                                        'subcat':subcat,
                                        'brand':brand})

@login_required(login_url='/login/')
def deleteproduct(request,id):
    product=Product.objects.get(id=id)
    product.delete()
    return HttpResponseRedirect("/sellerprofile/")

@login_required(login_url='/login/')
def wishlistpage(request,id):
    product=Product.objects.get(id=id)
    try:
        buyer=Buyer.objects.get(username=request.user)
    except:
        return HttpResponseRedirect("/sellerprofile/")
    wishlist=Wishlist.objects.filter(buyer=buyer)
    flag=False
    for i in wishlist:
        if(i.product==product):
            flag=True
            break
    if(flag==False):
        w=Wishlist()
        w.product=product
        w.buyer=buyer
        w.save()
    return HttpResponseRedirect('/buyerprofile/')

@login_required(login_url='/login/')
def deletewishlist(request,id):
    product=Wishlist.objects.get(id=id)
    buyer=Buyer.objects.get(username=request.user)
    if(product.buyer==buyer):
        product.delete()
    return HttpResponseRedirect('/buyerprofile/')
client=razorpay.Client(auth=(RAZORPAY_API_KEY,RAZORPAY_API_SECRET_KEY))
@login_required(login_url='/login/')
def checkout(request):
    cart=request.session.get('cart')
    product=[]
    sum=0
    dis=0
    user=Buyer.objects.get(username=request.user)
    if(request.method=='POST'):
        check=Checkout()
        check.buyer=user
        check.products=''
        check.total=0
        check.shipping=0
        check.finalAmount=0
        for i,j in cart.items():
            check.products=check.products+i+':'+str(j)+','
            p=Product.objects.get(id=i)
            check.total=p.finalprice*int(j)+check.total
        if(check.total<1000):
            check.shipping=50
        check.finalAmount=check.total+check.shipping
        mode=request.POST.get('mode')
        if(mode=='COD'):
            check.paymentStatus='2'
            check.save()
            request.session['flushcart']=True
            return HttpResponseRedirect('/confirm/')
        else:
            orderAmount=check.finalAmount*100
            orderCurrency='INR'
            paymentOrder=client.order.create(dict(amount=orderAmount,currency=orderCurrency,payment_capture=1))
            paymentID=paymentOrder['id']
            check.save()
            return render(request,'pay.html',{'amount':orderAmount,
                                              'api_key':RAZORPAY_API_KEY,
                                              'order_id':paymentID,
                                              'user':user})
    else:
        pass
    for i,j in cart.items():
        p=Product.objects.get(id=i)
        product.append(p)
        baseprice=p.baseprice
        sum=sum+int(baseprice)*int(j)
        dist=p.discount
        dis=dis+baseprice*int(j)*dist/100
    total=sum-dis
    if(total<3000):
        shipping=50
    else:
        shipping=0
    final=total+shipping
    info={'final':final,'total':total,'shipping':shipping}
    return render(request,'checkout.html',{'Product':product,'Data':user,'Info':info})
@login_required(login_url='/login/')
def paymentsuccess(request,oid,sid,pid):
    buyer=Buyer.objects.get(username=request.user)
    check=Checkout.objects.filter(buyer=buyer)
    check=check[::-1]
    check=check[0]
    check.orderId=oid
    check.paymentId=pid
    check.paymentsignature=sid
    check.paymentStatus='2'
    check.save()
    return HttpResponseRedirect('/confirm/')
@login_required(login_url='/login/')
def confirm(request):
    return render(request,'confirm.html')
def subcribepage(request):
    if(request.method=='POST'):
        email=request.POST.get('email')
        try:
            s=Subscribe.objects.get(email=email)
        except:
            sub=Subscribe()
            sub.email=email
            sub.save()
        return HttpResponseRedirect('/')
def contactus(request):
    if(request.method=='POST'):
        c=Contact()
        c.name=request.POST.get('name')
        c.email=request.POST.get('email')
        c.subject=request.POST.get('subject')
        c.mobile=request.POST.get('mobile')
        c.message=request.POST.get('message')
        c.save()
        messages.success(request,'Message Sent!!')
    return render(request,'ContactUs.html')
def forgetpassword(request):
    if(request.method=="POST"):
        username=request.POST.get('username')
        try:
            user=Buyer.objects.get(username=username)
        except:
            try:
                user=Seller.objects.get(username=username)
            except:
                messages.error(request,'Entered UserName Does not exist')
                return HttpResponseRedirect('/forgetpassword/') 
        user.otp=random.randint(1000,9999)
        user.save()
        subject = 'welcome to ONLINESHOP world'
        message = f'Hi {user.name}, Your OTP is {user.otp}.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user.email, ]
        send_mail( subject, message, email_from, recipient_list )
        #messages.success(request,'OTP send to Your registered Email ID') 
        return HttpResponseRedirect(f'/confirmOTP/{user.username}')      
    return render(request,'forgetpassword.html')
def confirmOTP(request,username):
    if(request.method=='POST'):
        try:
            user=Buyer.objects.get(username=username)
        except:
            user=Seller.objects.get(username=username)
        otp=int(request.POST.get('otp'))
        if(user.otp==otp):
            username=user.username
            pass1=request.POST.get('pass1')
            pass2=request.POST.get('pass2')
            if(pass1==pass2):
                user=User.objects.get(username=username)
                user.set_password(pass2)
                user.save()
                return HttpResponseRedirect('/login/')
        else:
            messages.error(request,'OTP is Invalid!')
    return render(request,'confirmOTP.html')

def deleteCheckout(request,id):
    check=Checkout.objects.get(id=id)
    user=Buyer.objects.get(username=request.user)
    if(check.buyer==user):
        check.delete()
    return HttpResponseRedirect('/buyerprofile/')

def paynow(request,id):
    cart=request.session.get('cart')
    product=[]
    sum=0
    dis=0
    user=Buyer.objects.get(username=request.user)
    if(request.method=='POST'):
        check=Checkout.objects.get(id=id)
        mode=request.POST.get('mode')
        if(mode=='COD'):
            check.paymentStatus='2'
            check.save()
            request.session['flushcart']=True
            return HttpResponseRedirect('/confirm/')
        else:
            orderAmount=check.finalAmount*100
            orderCurrency='INR'
            paymentOrder=client.order.create(dict(amount=orderAmount,currency=orderCurrency,payment_capture=1))
            paymentID=paymentOrder['id']
            check.save()
            return render(request,'pay.html',{'amount':orderAmount,
                                                'api_key':RAZORPAY_API_KEY,
                                                'order_id':paymentID,
                                                'user':user})
    else:
        pass
    for i,j in cart.items():
        p=Product.objects.get(id=i)
        product.append(p)
        baseprice=p.baseprice
        sum=sum+int(baseprice)*int(j)
        dist=p.discount
        dis=dis+baseprice*int(j)*dist/100
    total=sum-dis
    if(total<3000):
        shipping=50
    else:
        shipping=0
    final=total+shipping
    info={'final':final,'total':total,'shipping':shipping}
    return render(request,'checkout.html',{'Product':product,'Data':user,'Info':info})

from django import template
from numpy import integer, product
from mainApp.models import Product

register=template.Library()

@register.filter('cartQuantity')
def cartQuantity(request,id):
    cart=request.session.get('cart',None)
    for key,value in cart.items():
        if(key==str(id)):
            return value
@register.filter('cartfinal')
def cartfinal(request,id):
    cart=request.session.get('cart')
    for i,j in cart.items():
        if(i==str(id)):
            p=Product.objects.get(id=i)
            return p.finalprice*int(j)
@register.filter('paymentStatus')
def paymentStatus(request,num):
    if(num==1):
        return "Pending"
    else:
        return "Done"
@register.filter('orderStatus')
def orderStatus(reqeust,num):
    if(num==1):
        return "Not Packed"
    elif(num==2):
        return "Packed"
    elif(num==3):
        return "Out for Delivery"
    elif(num==4):
        return "Delivered"
@ register.filter('product')
def product(args):
    args=args[0:len(args)-1]    
    item=args.split(',')
    return item
@register.filter('productName')
def productName(args):
    try:
        item=args.split(':')
        if(item[0]!=''):
            item=int(item[0])
            p=Product.objects.get(id=item)
            return p.name
        else:
            return ''
    except:
        return ''

@register.filter('productImg')
def productImg(args):
    try:
        item=args.split(':')
        if(item[0]!=''):
                item=int(item[0])
                p=Product.objects.get(id=item)
                return p.pic1.url
        else:
            return ''
    except:
        return ''
@register.filter('productSize')
def productSize(args):
    try:
        item=args.split(':')
        if(item[0]!=''):
                item=int(item[0])
                p=Product.objects.get(id=item)
                return p.size
        else:
            return ''
    except:
        return ''
@register.filter('productPrice')
def productPrice(args):
    try:
        item=args.split(':')
        if(item[0]!=''):
                item=int(item[0])
                p=Product.objects.get(id=item)
                return p.finalprice
        else:
            return ''
    except:
        return ''
@register.filter('paymentmode')
def paymentmode(request,num):
    if(num==1):
        return 'Cash On Delivery'
    else:
        return 'Net Banking'
@register.filter('CheckoutStatus')
def CheckoutStatus(request,num):
    if(num==1):
        return True
    else:
        return False
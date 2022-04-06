"""OnlineShop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from mainApp import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
     path('',views.home),
    path('shop/<str:mc>/<str:sc>/<str:br>/',views.shop),
    path('productsection/<int:id>/',views.productsection),
    path('login/',views.login),
    path('logout/',views.logout),
    path('signup/',views.signup),
    path('sellerprofile/',views.profile),
    path('updateprofile/',views.updataprofile),
    path('addproduct/',views.AddProduct),
    path('editproduct/<int:id>',views.editproduct),
    path('deleteproduct/<int:id>',views.deleteproduct),
    path('buyerprofile/',views.buyerprofile),
    path('wishlist/<int:id>/',views.wishlistpage),
    path('deletewishlist/<int:id>/',views.deletewishlist),
    path('cart/',views.cart),
    path('deletecart/<str:id>/',views.deletecart),
    path('checkout/',views.checkout),
    path('confirm/',views.confirm),
    path('paymentSucess/',views.paymentsuccess),
    path('subscribe/',views.subcribepage),
    path('contactus/',views.contactus),
    path('forgetpassword/',views.forgetpassword),
    path('confirmOTP/<str:username>/',views.confirmOTP),
    path('deleteCheckout/<int:id>/',views.deleteCheckout),
    path('paynow/<int:id>/',views.paynow)
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

"""
URL configuration for Hello project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from store.views import index,about,contact,add_to_cart_view, update_item_quantity,cart_view,remove_from_cart_view,checkout_view,place_order_view,orders_view,search_view
from account.views import register_view,login_view,logout_view,reset_password_view
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = "IceCreams Corner Admin"
admin.site.site_title = "IceCreams Corner Admin Portal"
admin.site.index_title = "Welcome to IceCreams Corner "

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='home'),
    path('search/', search_view, name='search'),
    path('about/', about, name='about'),
    path('addtocart/', add_to_cart_view, name='addtocart'),
    path('updateitemquantity/', update_item_quantity, name='updateitemquantity'),
    path('removefromcart/', remove_from_cart_view, name='removefromcart'),
    path('cart/', cart_view, name='cart'),
    path('checkout/', checkout_view, name='checkout'),
    path('placeorder/', place_order_view, name='placeorder'),
    path('orders/', orders_view, name='orders'),
    path('contact/', contact, name='contact'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('resetpassword/', reset_password_view, name='resetpassword'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

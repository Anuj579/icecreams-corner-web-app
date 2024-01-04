from django.shortcuts import render,redirect
from store.models import Contact,IceCream,Cart,Order,OrderItem,Category
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

# Create your views here.
def get_all_categories(request):
    return {"categories": Category.objects.all()}

def get_cart_items_count(request):
    return {'cart_items_count': Cart.objects.filter(user_id= request.user.id).aggregate(Sum('quantity'))['quantity__sum']}
 
def index(request):
    if 'cid' in request.GET:
        return render(request, 'index.html', {'icecreams': IceCream.objects.filter(category_id= request.GET['cid']), 
        'is_any_popular_icecream': IceCream.objects.filter(sold_quantity__gt=5).exists(),
        'popular_icecreams': IceCream.objects.filter(sold_quantity__gt=5)})
    else:
        return render(request, 'index.html',{'icecreams': IceCream.objects.all(), 
        'is_any_popular_icecream': IceCream.objects.filter(sold_quantity__gt=5).exists(),
        'popular_icecreams': IceCream.objects.filter(sold_quantity__gt=5)})

def search_view(request):
    return render(request, 'index.html', {'icecreams': IceCream.objects.filter(name__icontains=request.GET['name']), 
                                          'popular_icecreams': IceCream.objects.filter(sold_quantity__gt=5)})

def about(request):
    return render(request, 'about.html')

def contact(request):
    if request.method== "POST":
        contact= Contact()
        contact.name= request.POST['name']
        contact.email =  request.POST['emailid']
        contact.phone = request.POST['phone']
        contact.desc= request.POST['desc']
        contact.date = datetime.today()
        contact.save()
        messages.success(request, 'Your message has been sent! We will contact you soon.')
    return render(request, 'contact.html')

@login_required(login_url='login')
def add_to_cart_view(request):
    icecream = IceCream.objects.get(id= request.POST['icecreamid'])
    if not Cart.objects.filter(icecream_id= request.POST['icecreamid'], user_id= request.user.id):
        cart= Cart()
        cart.quantity = int(request.POST['quantity'])
        cart.icecream = icecream
        cart.total = icecream.price * cart.quantity
        cart.user = User.objects.get(id= request.user.id)
        cart.save()
        return redirect('cart') 
    else:
        cart = Cart.objects.get(icecream_id = request.POST['icecreamid'], user_id= request.user.id)
        if cart.quantity<6:
            cart.quantity += int(request.POST['quantity'])
            if cart.quantity<=6:
                cart.total = icecream.price * cart.quantity
                cart.save()
                return redirect('cart') 
            else:
                messages.warning(request, 'You cannot add more than 6 quantities of this product')
                return redirect('home')
        else:
            messages.warning(request, 'You cannot add more than 6 quantities of this product')
            return redirect('home')
    

@login_required(login_url='login')
def update_item_quantity(request):
    if 'plus' in request.POST:
        cart_item = Cart.objects.get(icecream_id = request.POST['icecreamid'], user_id= request.user.id )
        if cart_item.quantity <6:
            cart_item.quantity+=1
            cart_item.total = cart_item.icecream.price * int(request.POST['quantity'])
            cart_item.save()
        else:
            messages.warning(request,'You cannot add more than 6 quantities of this product')
    elif 'minus' in request.POST:
        cart_item = Cart.objects.get(icecream_id = request.POST['icecreamid'], user_id= request.user.id)
        if cart_item.quantity >1 :
            cart_item.quantity-=1
            cart_item.total = cart_item.icecream.price * int(request.POST['quantity'])
            cart_item.save()
        else:
            cart_item.delete()
    return redirect('cart')


@login_required(login_url='login')
def cart_view(request):
    return render(request, 'cart.html',{'is_any_cart_item': Cart.objects.filter(user_id=request.user.id).exists(), 
                                        'cart_items':Cart.objects.filter(user_id= request.user.id),
                                        'grand_total':Cart.objects.filter(user_id= request.user.id).aggregate(Sum('total'))['total__sum']})

@login_required(login_url='login')
def remove_from_cart_view(request):
    cart_items = Cart.objects.filter(icecream_id=request.POST['icecreamid'],
    user_id=request.user.id)
    cart_items.delete()
    return redirect('cart')

@login_required(login_url='login')
def checkout_view(request):
    return render(request, 'checkout.html', {'grand_total':request.POST['grandtotal']})

def place_order_view(request):
    order= Order()
    order.total = request.POST['amounttopay']
    order.address = request.POST['address']
    order.phone_number = request.POST['phonenumber']
    order.user = request.user
    order.save()

    cart_items = Cart.objects.filter(user_id=request.user.id)

    for cart_item in cart_items:
        order_item = OrderItem()
        order_item.quantity= cart_item.quantity
        order_item.total = cart_item.total
        order_item.icecream = IceCream.objects.get(id= cart_item.icecream_id)
       
        icecream = IceCream.objects.get(id= cart_item.icecream_id)
        # Update sold_quantity for the ice cream
        icecream.sold_quantity += cart_item.quantity
        icecream.save()

        order_item.user = request.user
        order_item.order = order
        order_item.save()
        cart_item.delete()

    return redirect('orders')

@login_required(login_url='login')
def orders_view(request):
    return render(request, 'orders.html', {'is_any_order' : Order.objects.filter(user_id=request.user.id).exists(),
     'orders': Order.objects.filter(user_id=request.user.id).order_by('-date'),
     'order_items': OrderItem.objects.filter(user_id=request.user.id)
     })
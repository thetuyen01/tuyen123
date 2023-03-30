from django.shortcuts import render, HttpResponse, redirect
from category.models import Category
from product.models import Product, Comment
from cart.models import Cart, OrtherItem
from shippingaddress.models import ShippingAddress, PurchaseHistory
from django.shortcuts import get_object_or_404
from django.db.models import Q
from account.models import customeruser


def index(request):
    if request.method=="GET":
        user = request.user
        categorys = Category.objects.all()
        if request.user.is_authenticated:
            cart_ = Cart.objects.get(user = user)
            orderitems = OrtherItem.objects.filter(cart = cart_)
            count = orderitems.count()
            return render(request, 'core/home.html',{'categorys':categorys,'user':user,'count':count})
        else:
            count = 0
            return render(request, 'core/home.html',{'categorys':categorys,'user':user,'count':count})
    else:
        return redirect('core:index')



def ViewCategory(request, slug):
    if request.method == "GET":
        categorys = Category.objects.all()
        obj = get_object_or_404(Category, slug=slug)
        products = Product.objects.filter(category = obj)
        if request.user.is_authenticated:
            user = request.user
            cart_ = Cart.objects.get(user = user)
            orderitems = OrtherItem.objects.filter(cart = cart_)
            count = orderitems.count()
            return render(request, 'core/product.html',{'products':products,'categorys':categorys,'obj':obj,'count':count})
        else:
            count = 0
            return render(request, 'core/product.html',{'products':products,'categorys':categorys,'obj':obj,'count':count})
    else:
        return redirect('core:index')


# serach product

def serach(request):
    if request.method == "GET":
        q = request.GET.get('q')
        if q :
            products = Product.objects.filter(Q(name__icontains = q.lower())|Q(name__startswith=q.lower())|Q(name__endswith=q.lower()))
            return render(request, 'core/productall.html',{"products":products,'q':q})
        else:
            products = Product.objects.all()
            return render(request, 'core/productall.html',{"products":products,'q':q})

# product one

def oneproduct(request, id):
    if request.method == "GET":
        product = get_object_or_404(Product, id=id)
        comt = Comment.objects.filter(product=product)
        if request.user.is_authenticated:
            user = request.user
            cart_ = Cart.objects.get(user = user)
            orderitems = OrtherItem.objects.filter(cart = cart_)
            count = orderitems.count()
            return render(request, 'core/productone.html',{'product':product,'count':count,'comt':comt})
        else:
            count = 0
            return render(request, 'core/productone.html',{'product':product,'count':count,'comt':comt})
    else:
        return redirect('core:index')
    


# cart

def cart__(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            user = request.user
            cart_ = Cart.objects.get(user = user)
            orderitems = OrtherItem.objects.filter(cart = cart_)
            count = orderitems.count()
            return render(request, 'core/cart.html',{'orderitems':orderitems,'cart':cart_,'count':count})
        # delete Orderitem
        if request.method == "POST":
            id= request.POST.get("id")
            OrtherItem.objects.get(id=id).delete()
            return redirect('core:cart')
    else:
        return redirect('account:login')
    

# add orderitem

def addorderitem(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            user = request.user
            cart = get_object_or_404(Cart, user=user)
            id = request.POST.get('id')
            quantity = request.POST.get('quantity')
            product = get_object_or_404(Product, id=id)
            OrtherItem.objects.create(cart=cart, product=product,quantity=quantity)
            return redirect('core:cart')
    else:
        return redirect('account:login')
    

# delete orderitem
def edititem(request, id):
    if request.user.is_authenticated:
        if request.method == "GET":
            oderitem = get_object_or_404(OrtherItem, id=id)
            return render(request, 'core/edit.html',{'oderitem':oderitem})
        if request.method == "POST":
            quantity = request.POST.get('quantity')
            oderitem = get_object_or_404(OrtherItem, id=id)
            oderitem.quantity = quantity
            oderitem.save()
            return redirect('core:cart')
    else:
        return redirect('account:login')

# checkout
def checkout(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            user = request.user
            cart = Cart.objects.get(user=user)
            orderitems = OrtherItem.objects.filter(cart = cart)
            count = orderitems.count()
            return render(request, 'core/checkout.html',{'orderitems':orderitems,'cart':cart,'count':count})
        if request.method == "POST":
            name = request.POST.get('name')
            email = request.POST.get('email')
            number = request.POST.get('number')
            address = request.POST.get('address')
            if name != "" and email != "" and number != "" and address != ""  :
                user = request.user
                cart = Cart.objects.get(user=user)
                order = OrtherItem.objects.filter(cart=cart)
                if order:
                    description=""
                    total = 0
                    item = 0
                    for total_price in order:
                        description+=str(total_price.product.name)+" : $"+str(total_price.product.price)+" ,"
                        item+=total_price.quantity
                        total+=int(total_price.quantity)*int(total_price.product.price)
                    shippings=ShippingAddress.objects.create(user=user, cart=cart, total_items=item, total=total, description=description, email=email, 
                                            adderss=address, mobile=number, name=name)
                    for i in order:
                        id = i.product.pk
                        product = get_object_or_404(Product, id=id)
                        product.hasbeensell = product.hasbeensell +1
                        product.save()
                    order.delete()
                else:
                    return redirect('core:checkout')
                return redirect('core:pending')
            else:
                return redirect('core:checkout')
    else:
        return redirect('account:login')
        

# pending
def pending(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            shippings = ShippingAddress.objects.filter(user=request.user)
            user = request.user
            cart_ = Cart.objects.get(user = user)
            orderitems = OrtherItem.objects.filter(cart = cart_)
            count = orderitems.count()
            return render(request, 'core/pending.html',{'shippings':shippings,'count':count})
        if request.method == "POST":
            shippings = ShippingAddress.objects.get(id=request.POST.get('id'))
            if shippings.received == False:
                return redirect('core:pending')
            else:
                PurchaseHistory.objects.create(user=request.user, total_items=shippings.total_items, total=shippings.total,
                                description=shippings.description, adderss=shippings.adderss, email=shippings.email, mobile=shippings.mobile)
                shippings.delete()
                return redirect('core:pending')
    else:
        return redirect('account:login')
        

# profile

def profile(request):
    if request.user.is_authenticated:
        user = request.user
        customer = customeruser.objects.get(user=user)
        purchs = PurchaseHistory.objects.filter(user=user)
        cart_ = Cart.objects.get(user = user)
        orderitems = OrtherItem.objects.filter(cart = cart_)
        count = orderitems.count()
        return render(request, 'core/profile.html',{'user':user,'purchs':purchs,'count':count,'customer':customer})
    else:
        return redirect('account:login')
    

# comment
def comment_(request):
    if request.user.is_authenticated:
        id = request.POST.get('id')
        if request.POST.get('id') != "" and request.POST.get('number') !="" and request.POST.get('bl')!="":
            number_star = request.POST.get('number')
            cm = request.POST.get('bl')
            product = get_object_or_404(Product, id = id)
            user = request.user
            comt = Comment.objects.create(user =user, product=product, comment=cm, star=number_star)
            comt.save()
            count_ = Comment.objects.count()
            sao = (float(count_-1)*(product.evaluate)+float(number_star))/count_
            sao = round(sao, 2)
            product.evaluate = sao
            product.save()
            return redirect('core:oneproduct', id=id)
        else:
            return redirect('core:oneproduct', id=id)
    else:
        return redirect('account:login')


# contact
def contact(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            user = request.user
            cart_ = Cart.objects.get(user = user)
            orderitems = OrtherItem.objects.filter(cart = cart_)
            count = orderitems.count()
            return render(request, 'core/contact.html',{'count':count})
        else:
            return redirect('account:login')
    else:
        return redirect('core:index')
    
# updateprofile

def updateprofile(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            user = request.user
            cart_ = Cart.objects.get(user = user)
            orderitems = OrtherItem.objects.filter(cart = cart_)
            count = orderitems.count()
            return render(request, 'core/updateprofile.html',{'count':count})
        if request.method == "POST":
            name = request.POST.get('name')
            numberphone = request.POST.get('numberphone')
            address = request.POST.get('address')
            if name !="" and numberphone !="" and address !="":
                user = request.user
                customer = customeruser.objects.get(user=user)
                customer.name = name
                customer.number_phone = numberphone
                customer.address = address
                customer.save()
                return redirect('core:profile')
            else:
                return redirect('core:updateprofile')
    else:
        return redirect('account:login')
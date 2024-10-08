from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse,reverse_lazy
from django.views.generic import TemplateView, ListView, DeleteView, DetailView
from app.models import Book
from .models import Cart,CartItem
from django.conf import settings
import stripe
from django.db.models.query import Q

# Create your views here.


def register_user(request):

    role = request.GET.get('admin')

    if request.method =='POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        is_superuser = role
        password = request.POST.get('pass')
        cpass = request.POST.get('cpass')

        if cpass != password:
            messages.info(request,'Password mismatch')
            return redirect('register')
        
        if User.objects.filter(username = username).exists():
            messages.info(request,'Username already exists')
            return redirect('register')
        if User.objects.filter(email = email).exists():
            messages.info(request,'Email already exists')
            return redirect('register')
        user = User.objects.create_user(username=username, first_name= first_name, last_name = last_name, is_superuser = is_superuser, password= password, email=email)
        user.save()
        return redirect('login')
    
    return render(request, 'users/register.html')

def login_user(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('pass')

        user = authenticate(username=username, password= password)
        try:
            if user is not None:
                admin = user.is_superuser
                if not admin:
                    login(request,user)
                    return redirect('user_list_book')
                elif admin:
                    login(request,user)
                    return redirect('list_book')
            else:
                messages.info(request,'Invalid Credentials')
                return redirect('login')
        except:
            messages.error(request,'Invalid Role')
    
    return render(request,'users/login.html')


class Test(TemplateView):

    template_name = 'users/base.html'

def logout_user(request):

    logout(request)
    return redirect('login')

class ListUser(ListView):

    model = User

    template_name = 'admin/list_users.html'

    context_object_name = 'users'

    paginate_by = 10

def update_user(request,pk):

    user = User.objects.get(pk=pk)

    if request.method == 'POST':

        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        is_superuser = request.POST.get('is_superuser')
        
        if User.objects.exclude(pk=pk).filter(username = username).exists():
            messages.info(request,'Username already exists')
            return redirect(reverse('update_user',kwargs={'pk':user.pk}))
        if User.objects.exclude(pk=pk).filter(email = email).exists():
            messages.info(request,'Email already exists')
            return redirect(reverse('update_user',kwargs={'pk':user.pk}))
        user.username = username
        user.first_name = first_name
        user.last_name  = last_name
        user.email = email
        user.is_superuser = is_superuser
        user.save()
        return redirect('list_user')
    
    return render(request, 'admin/update_user.html',{'user':user})

class DeleteUser(DeleteView):

    model = User
    template_name = 'admin/delete_user.html'
    success_url = reverse_lazy('list_user')

class ListBook(ListView):

    model = Book
    template_name = 'users/list_book.html'
    context_object_name = 'books'
    paginate_by = 10

def add_to_cart_from_list(request, book_id):


    if request.method == 'POST':

        book = Book.objects.get(id=book_id)

        if book.quantity > 0:
            cart,created = Cart.objects.get_or_create(user = request.user)
            cart_item,item_created = CartItem.objects.get_or_create(cart=cart, book = book)

            if not item_created:
                cart_item.quantity += 1
                cart_item.save()
        
        else:
            messages.error(request, 'Book is unavailable at the moment')

        return redirect('user_list_book')
    
def add_to_cart_from_details(request, book_id):


    if request.method == 'POST':

        book = Book.objects.get(id=book_id)

        if book.quantity > 0:
            cart,created = Cart.objects.get_or_create(user = request.user)
            cart_item,item_created = CartItem.objects.get_or_create(cart=cart, book = book)

            if not item_created:
                cart_item.quantity += 1
                cart_item.save()
        
        else:
            messages.error(request, 'Book is unavailable at the moment')

        return redirect('user_book_detail')
    
class BookDetail(DetailView):

    model = Book

    template_name ='users/book_detail.html'

    context_object_name = 'book'

def view_cart(request):

    cart,_ = Cart.objects.get_or_create(user = request.user)
    cart_items = cart.cartitem_set.all()
    print(cart_items)
    if cart_items:
        total_price = sum(item.book.price * item.quantity for item in cart_items)
        context = {'cart_items':cart_items,'total_price':total_price}

    else:
        context = {'cart_items':[], 'total_price':0}

    return render(request, 'users/view_cart.html', context=context)

def increase_quantity(request,item_id):

    if request.method == 'POST':
        cart_item = CartItem.objects.get(id = item_id)

        if cart_item.book.quantity >0 and cart_item.quantity < 6:

            cart_item.quantity += 1
            cart_item.save()

        return redirect('view_cart')

def decrease_quantity(request,item_id):

    if request.method =='POST':

        cart_item = CartItem.objects.get(id = item_id)

        if cart_item.quantity > 1:

            cart_item.quantity -= 1
            cart_item.save()

        return redirect('view_cart')

def remove_item(request,item_id):

    if request.method == 'POST':
        try:
            cart_item = CartItem.objects.get(id = item_id)
            cart_item.delete()
            return redirect('view_cart')

        except cart_item.DoesNotExist:
            pass

def create_checkout_session(request):

    cart = Cart.objects.get(user = request.user)
    cart_items = cart.cartitem_set.all()

    if cart_items:
        stripe.api_key = settings.STRIPE_SECRET_KEY

        if request.method == 'POST':

            line_items = []

            for cart_item in cart_items:
                if cart_item.book:
                    line_item ={
                        'price_data':{
                            'currency': 'INR',
                            'unit_amount':int(cart_item.book.price * 100),
                            'product_data':{
                                'name':cart_item.book.title
                            },
                        },
                        'quantity':cart_item.quantity 
                    }
                    line_items.append(line_item)

            if line_items:

                checkout_session = stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=line_items,
                    mode='payment',
                    success_url=request.build_absolute_uri(reverse('success')),
                    cancel_url=request.build_absolute_uri(reverse('cancel')),
                )

                return redirect(checkout_session.url,code=303)
            
def success(request):
    cart = Cart.objects.get(user = request.user)
    cart_items = cart.cartitem_set.all()

    for cart_item in cart_items:
        product = cart_item.book

        product.quantity -= cart_item.quantity
        product.save()

    cart_items.delete()

    return render(request, 'users/success.html')

def cancel(request):
    return render(request,'users/cancel.html')

class SearchBook(ListView):

    model = Book
    template_name = 'users/search_book.html'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q')

        return Book.objects.filter(
            Q(title__icontains = query) |
            Q(author__author__icontains = query)
        )


        
        



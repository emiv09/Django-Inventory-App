from django.shortcuts import render, redirect
from .form import ProductForm
from .models import Product
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test

# Create your views here.

#Register view
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request,'accounts/login.html')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.POST.get('next') or request.GET.get('next') or 'home'
            return redirect(next_url)
        else:
            error_message = "Invalid Credentials"
            return render(request, "accounts/login.html", {"error" : error_message})
    return render(request, "accounts/login.html")


def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect('login')
    else: 
        return redirect('home')


@login_required
def home_view(request):
    return render(request, 'invApp/home.html')

@login_required
# Create View
def product_create_view(request):
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')
        
    return render(request, 'invApp/product_form.html', {'form': form})

@login_required
# Read View
def product_list_view(request):
    products = Product.objects.all()
    return render(request, 'invApp/product_list.html', {'products': products})

@login_required
# Update view
def product_update_view(request, product_id):
    product = Product.objects.get(product_id=product_id)
    form = ProductForm(instance=product)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    return render(request, 'invApp/product_form.html', {'form': form})

def is_admin_or_staff(user):
    return user.is_staff or user.is_superuser


@login_required
# Delete view
def product_delete_view(request, product_id):
    product = Product.objects.get(product_id=product_id)
    if request.method == 'POST':
        if(is_admin_or_staff(request.user)):
            product.delete()
            return redirect('product_list')
        else:
            error_message = "You do not have permission to delete products"
            return render(request, 'invApp/product_confirm_delete.html', {'product': product, 'error': error_message})
    return render(request, 'invApp/product_confirm_delete.html', {'product': product})



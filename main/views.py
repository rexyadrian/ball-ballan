import datetime
from django.http import HttpResponse
from django.core import serializers
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from main.forms import ProductForm, StoreForm
from main.models import Product, Store

@login_required(login_url='/login')
def show_main(request):

    filter_type = request.GET.get("filter", "all")  # default 'all'

    if filter_type == "all":
        product_list = Product.objects.all()
    else:
        product_list = Product.objects.filter(user=request.user)
    
    context = {
        'app_name' : 'Ball-Ballan',
        'npm' : '2406495666',
        'name': request.user.username,
        'class': 'PBP D',
        'product_list': product_list,
        'last_login': request.COOKIES.get('last_login', 'Never'),
    }

    return render(request, "main.html", context)

def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login_user')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                errors = {
                    field: [str(e) for e in errs] for field, errs in form.errors.items()
                }
                return JsonResponse({'success': False, 'error': errors})

    context = {
        'form': form
    }
    return render(request, 'register.html', context)

@csrf_exempt
def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            response = JsonResponse({"success": True})
            response.set_cookie("last_login", str(datetime.datetime.now()))
            return response
        else:
            return JsonResponse({
                "success": False,
                "error": "Username or Password is incorrect."
            }, status=400)
  
    return render(request, "login.html")

@csrf_exempt
def logout_user(request):
    logout(request)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({"success": True})
    response = HttpResponseRedirect(reverse("main:login"))
    response.delete_cookie("last_login")
    return response

def create_store(request):
    form = StoreForm(request.POST or None, request.FILES or None)

    # cek apakah user sudah punya store
    if hasattr(request.user, 'store'):
        return redirect('main:show_store', user_id=request.user.id)

    if form.is_valid() and request.method == "POST":
        store_entry = form.save(commit=False)
        store_entry.user = request.user
        store_entry.save()
        return redirect('main:show_store', user_id=request.user.id)

    context = {
        'form': form
    }
    return render(request, "create_store.html", context)

def show_store(request, user_id):
    store = get_object_or_404(Store, user__id=user_id)
    products = store.products.all()

    context = {
        'store': store,
        'products': products
    }
    return render(request, "store_detail.html", context)

# Add Product
def add_product(request):
    try:
        store = request.user.store
    except Store.DoesNotExist:
        messages.warning(request, "Kamu harus membuat toko terlebih dahulu sebelum menambah produk.")
        return redirect('main:create_store')

    form = ProductForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        product_entry = form.save(commit = False)
        product_entry.user = request.user
        product_entry.store = store
        product_entry.save()
        return redirect('main:show_main')

    context = {
        'form': form,
        'store': store,
    }
    return render(request, "add_product.html", context)

@login_required(login_url='/login')
def show_product(request, id):
    product = get_object_or_404(Product, pk=id)

    context = {
        'product': product
    }
    return render(request, "product_detail.html", context)

def edit_product(request, id):
    product = get_object_or_404(Product, pk=id)
    form = ProductForm(request.POST or None, instance=product)
    if form.is_valid() and request.method == 'POST':
        form.save()
        return redirect('main:show_main')

    context = {
        'form': form
    }

    return render(request, "edit_product.html", context)

def delete_product(request, id):
    product = get_object_or_404(Product, pk=id)
    product.delete()
    return HttpResponseRedirect(reverse('main:show_main'))

def show_xml(request):
    product_list = Product.objects.all()
    xml_data = serializers.serialize("xml", product_list)
    return HttpResponse(xml_data, content_type="application/xml")

def show_json(request):
    product_list = Product.objects.all()
    data = [
        {
            'id': str(product.id),
            'name': product.name,
            'price': product.price,
            'description': product.description,
            'thumbnail': product.thumbnail,
            'category': product.category,
            'is_featured': product.is_featured,
            'stock': product.stock,
            'brand': product.brand,
            'sold': product.sold,
            'user_id': product.user_id,
            "store": {
                "name": product.store.name if product.store else None,
                "address": product.store.address if product.store else None,
                "profile": product.store.profile if product.store else None,
            }
        }
        for product in product_list
    ]

    return JsonResponse(data, safe=False)

def show_xml_by_id(request, id):
    try:
       product_item = Product.objects.filter(pk=id)
       xml_data = serializers.serialize("xml", product_item)
       return HttpResponse(xml_data, content_type="application/xml")
    except Product.DoesNotExist:
       return HttpResponse(status=404)

def show_json_by_id(request, id):
    try:
        product = Product.objects.select_related('user').get(pk=id)
        data = {
            'id': str(product.id),
            'name': product.name,
            'price': product.price,
            'description': product.description,
            'thumbnail': product.thumbnail,
            'category': product.category,
            'is_featured': product.is_featured,
            'stock': product.stock,
            'brand': product.brand,
            'sold': product.sold,
            'user_id': product.user_id,
            "store": {
                "id": product.store.user.id if product.store.user else None,
                "name": product.store.name if product.store else None,
                "address": product.store.address if product.store else None,
                "profile": product.store.profile if product.store else None,
            }
        }
        return JsonResponse(data)
    except Product.DoesNotExist:
        return JsonResponse({'detail': 'Not found'}, status=404)
    
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import Product, Store

@csrf_exempt
@require_POST
def add_product_ajax(request):
    user = request.user

    try:
        store = user.store
    except Store.DoesNotExist:
        return HttpResponse(b"STORE_NOT_FOUND", status=400)

    name = request.POST.get("name")
    price = request.POST.get("price")
    description = request.POST.get("description")
    category = request.POST.get("category")
    thumbnail = request.POST.get("thumbnail")
    is_featured = request.POST.get("is_featured") == "on"
    stock = request.POST.get("stock")
    brand = request.POST.get("brand")

    if not all([name, price, description, category, stock, brand]):
        return HttpResponse(b"INVALID_DATA", status=400)

    new_product = Product(
        user=user,
        store=store,
        name=name,
        price=int(price),
        description=description,
        category=category,
        thumbnail=thumbnail or None,
        is_featured=is_featured,
        stock=int(stock),
        brand=brand
    )
    new_product.save()

    return HttpResponse(b"CREATED", status=201)
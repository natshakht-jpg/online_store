from django.shortcuts import render
from django.http import HttpResponse
from .models import Product, Contact
from django.shortcuts import redirect
from .forms import ProductForm
from django.core.paginator import Paginator

def home(request):
    products = Product.objects.all()
    paginator = Paginator(products, 3)  # 3 товара на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'catalog/home.html', {'page_obj': page_obj})

def contacts(request):
    contact = Contact.objects.first()
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'Имя: {name}, Телефон: {phone}, Сообщение: {message}')
        return HttpResponse('Спасибо, ваше сообщение отправлено!')
    return render(request, 'catalog/contacts.html', {'contact': contact})

def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    return render(request, 'catalog/product_detail.html', {'product': product})

def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = ProductForm()
    return render(request, 'catalog/product_form.html', {'form': form})

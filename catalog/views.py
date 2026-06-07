from django.shortcuts import render
from django.http import HttpResponse
from .models import Product, Contact

def home(request):
    last_products = Product.objects.all().order_by('-created_at')[:5]
    print("Последние 5 продуктов:")
    for p in last_products:
        print(f"{p.name} - {p.price}")
    return render(request, 'catalog/home.html', {'last_products': last_products})

def contacts(request):
    contact = Contact.objects.first()
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'Имя: {name}, Телефон: {phone}, Сообщение: {message}')
        return HttpResponse('Спасибо, ваше сообщение отправлено!')
    return render(request, 'catalog/contacts.html', {'contact': contact})
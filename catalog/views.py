from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, TemplateView, UpdateView, DeleteView
from .models import Product, Contact
from .forms import ProductForm
from django.core.paginator import Paginator
from django.urls import reverse_lazy

class ProductListView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = self.get_queryset()
        paginator = Paginator(products, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

class ContactView(TemplateView):
    template_name = 'catalog/contacts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contact'] = Contact.objects.first()
        return context

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'Имя: {name}, Телефон: {phone}, Сообщение: {message}')
        return HttpResponse('Спасибо, ваше сообщение отправлено!')

def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            # Дополнительная проверка запрещённых слов
            name = form.cleaned_data.get('name')
            description = form.cleaned_data.get('description')
            forbidden = ['казино', 'криптовалют', 'крипт', 'бирж', 'дешев', 'бесплатн', 'обман', 'полиц', 'радар']
            for word in forbidden:
                if word in name.lower():
                    form.add_error('name', f'Название не должно содержать слово "{word}"')
                    has_error = True
                if description and word in description.lower():
                    form.add_error('description', f'Описание не должно содержать слово "{word}"')
                    has_error = True
            if not has_error:
                form.save()
                return redirect('/')
    else:
        form = ProductForm()
    return render(request, 'catalog/product_form.html', {'form': form})

class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('home')

class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('home')

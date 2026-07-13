from django.http import HttpResponse, HttpResponseForbidden
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from .models import Product, Contact, Category
from .forms import ProductForm
from django.core.cache import cache
from .services import get_products_by_category
from .services import get_products_from_cache

class ProductListView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'
    paginate_by = 3

    def get_queryset(self):
        return get_products_from_cache()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = self.get_queryset()
        paginator = Paginator(products, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        return context

@method_decorator(cache_page(60 * 15), name='dispatch')
class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:home')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.owner != request.user and not request.user.is_superuser:
            return HttpResponseForbidden('Вы не владелец этого продукта')
        return super().dispatch(request, *args, **kwargs)

class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:home')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.owner != request.user and not request.user.is_superuser and not request.user.has_perm('catalog.can_unpublish_product'):
            return HttpResponseForbidden('У вас нет прав на удаление этого продукта')
        return super().dispatch(request, *args, **kwargs)

class CategoryProductsView(ListView):
    template_name = 'catalog/category_products.html'
    context_object_name = 'products'

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        return get_products_by_category(category_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        try:
            category = Category.objects.get(id=category_id)
            context['category_name'] = category.name
        except Category.DoesNotExist:
            context['category_name'] = 'Неизвестная категория'
        return context

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

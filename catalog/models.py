from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='наименование')
    description = models.TextField(verbose_name='описание', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name='наименование')
    description = models.TextField(verbose_name='описание')
    image = models.ImageField(upload_to='products/', verbose_name='изображение', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='категория')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='цена за покупку')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='дата последнего изменения')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'

class Contact(models.Model):
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    email = models.EmailField(verbose_name='Email')
    address = models.TextField(verbose_name='Адрес')

    def __str__(self):
        return self.phone

    class Meta:
        verbose_name = 'контакт'
        verbose_name_plural = 'контакты'

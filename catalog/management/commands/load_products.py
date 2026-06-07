from django.core.management.base import BaseCommand
from django.core.management import call_command
from catalog.models import Category, Product

class Command(BaseCommand):
    help = 'Очищает базу и загружает данные из фикстур'

    def handle(self, *args, **options):
        self.stdout.write('Очистка...')
        Category.objects.all().delete()
        Product.objects.all().delete()

        self.stdout.write('Загрузка категорий...')
        call_command('loaddata', 'catalog/fixtures/categories.json')

        self.stdout.write('Загрузка продуктов...')
        call_command('loaddata', 'catalog/fixtures/products.json')

        self.stdout.write('Готово!')
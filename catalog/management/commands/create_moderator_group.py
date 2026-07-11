from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from catalog.models import Product

class Command(BaseCommand):
    help = 'Создаёт группу "Модератор продуктов" и назначает права'

    def handle(self, *args, **options):
        # Получаем тип контента для модели Product
        content_type = ContentType.objects.get_for_model(Product)

        # Получаем права
        can_unpublish = Permission.objects.get(
            codename='can_unpublish_product',
            content_type=content_type
        )
        can_delete = Permission.objects.get(
            codename='delete_product',
            content_type=content_type
        )

        # Создаём группу
        group, created = Group.objects.get_or_create(name='Модератор продуктов')

        if created:
            self.stdout.write('Группа "Модератор продуктов" создана')
        else:
            self.stdout.write('Группа "Модератор продуктов" уже существует')

        # Назначаем права группе
        group.permissions.add(can_unpublish, can_delete)
        self.stdout.write('Права назначены группе')

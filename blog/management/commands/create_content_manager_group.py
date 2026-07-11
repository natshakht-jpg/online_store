from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from blog.models import BlogPost

class Command(BaseCommand):
    help = 'Создаёт группу "Контент-менеджер" и назначает права на блог'

    def handle(self, *args, **options):
        # Получаем тип контента для модели BlogPost
        content_type = ContentType.objects.get_for_model(BlogPost)

        # Получаем права на блог
        add_perm = Permission.objects.get(codename='add_blogpost', content_type=content_type)
        change_perm = Permission.objects.get(codename='change_blogpost', content_type=content_type)
        delete_perm = Permission.objects.get(codename='delete_blogpost', content_type=content_type)

        # Создаём группу
        group, created = Group.objects.get_or_create(name='Контент-менеджер')

        if created:
            self.stdout.write('Группа "Контент-менеджер" создана')
        else:
            self.stdout.write('Группа "Контент-менеджер" уже существует')

        # Назначаем права группе
        group.permissions.add(add_perm, change_perm, delete_perm)
        self.stdout.write('Права на блог назначены группе')

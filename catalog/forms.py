from django import forms
from django.core.exceptions import ValidationError
from .models import Product

# Список запрещённых слов (все в нижнем регистре)
FORBIDDEN_WORDS = [
    'казино', 'криптовалюта', 'крипта', 'биржа',
    'дешево', 'бесплатно', 'обман', 'полиция', 'радар'
]


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category', 'image']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            return name
        name_lower = name.lower()
        for word in FORBIDDEN_WORDS:
            if word in name_lower:
                raise ValidationError(f'Название не должно содержать слово "{word}"')
        return name

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if description:
            desc_lower = description.lower()
            for word in FORBIDDEN_WORDS:
                if word in desc_lower:
                    raise ValidationError(f'Описание не должно содержать слово "{word}"')
        return description

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price < 0:
            raise ValidationError('Цена не может быть отрицательной')
        return price

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            # Проверка размера (не более 5 МБ)
            if image.size > 5 * 1024 * 1024:
                raise ValidationError('Размер изображения не должен превышать 5 МБ')

            # Проверка формата
            import os
            ext = os.path.splitext(image.name)[1].lower()
            if ext not in ['.jpg', '.jpeg', '.png']:
                raise ValidationError('Разрешены только изображения форматов JPEG, JPG, PNG')
        return image

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Стилизация всех полей
        for field_name, field in self.fields.items():
            # Если поле — чекбокс (например, булево поле)
            if field.widget.__class__.__name__ == 'CheckboxInput':
                field.widget.attrs['class'] = 'form-check-input'
            else:
                # Все остальные поля получают класс form-control
                field.widget.attrs['class'] = 'form-control'

            # Плейсхолдеры
            if field_name == 'name':
                field.widget.attrs['placeholder'] = 'Введите название товара'
            elif field_name == 'description':
                field.widget.attrs['placeholder'] = 'Введите описание товара'
            elif field_name == 'price':
                field.widget.attrs['placeholder'] = 'Введите цену'
            elif field_name == 'category':
                field.widget.attrs['placeholder'] = 'Выберите категорию'
            elif field_name == 'image':
                field.widget.attrs['placeholder'] = 'Выберите изображение'

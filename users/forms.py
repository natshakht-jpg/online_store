from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Убираем стандартные подсказки к полям пароля
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''

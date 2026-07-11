from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login
from django.core.mail import send_mail
from .forms import UserRegistrationForm
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User
from django.urls import reverse_lazy

class RegisterView(View):
    form_class = UserRegistrationForm
    template_name = 'users/register.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            # Отправка приветственного письма
            send_mail(
                subject='Добро пожаловать!',
                message='Вы успешно зарегистрировались на нашем сайте.',
                from_email=None,
                recipient_list=[user.email],
                fail_silently=True,
            )
            return redirect('catalog:home')
        return render(request, self.template_name, {'form': form})

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['avatar', 'phone', 'country']
    template_name = 'users/profile_edit.html'
    success_url = reverse_lazy('home')

    def get_object(self):
        return self.request.user
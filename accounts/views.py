from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from .forms import AuthenticationForm
from django.views.generic import View, FormView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from .models import User
from django.contrib import messages
from .forms import EmailAuthenticationForm, RegisterForm
from django.contrib.messages.views import SuccessMessageMixin


class LoginClassView(LoginView):
    template_name = 'home/index.html'
    redirect_authenticated_user = True
    form_class = EmailAuthenticationForm

    def form_valid(self, form):
        login(self.request, form.get_user())
        messages.success(self.request, 'خوش آمدید')
        return redirect('/')

    def form_invalid(self, form):

        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, error)

        redirect_url = self.request.META.get('HTTP_REFERER', '/')
        return redirect(f"{redirect_url}?modal=login")


class RegisterView(SuccessMessageMixin, FormView):
    template_name = "home/index.html"
    form_class = RegisterForm
    success_url = reverse_lazy("home:index")
    success_message = 'ثبت نام شما با موفقیت انجام شد'

    def form_valid(self, form):
        user = User.objects.create_user(
            email=form.cleaned_data["email"],
            password=form.cleaned_data["password"],
        )
        login(self.request, user)
        return super().form_valid(form)

    def form_invalid(self, form):

        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, error)

        redirect_url = self.request.META.get('HTTP_REFERER', '/')
        return redirect(f"{redirect_url}?modal=register")


class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect('home:index')

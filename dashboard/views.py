from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, View, UpdateView
from django.urls import reverse_lazy
from .forms import UserAddressForm, UserProfileForm
from .models import UserAddressModel
from accounts.models import Profile


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/include/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user

        return context


class AddressListView(LoginRequiredMixin, ListView):
    model = UserAddressModel

    template_name = "dashboard/user-address.html"

    context_object_name = "addresses"

    login_url = "accounts:login"

    def get_queryset(self):
        return UserAddressModel.objects.filter(
            user=self.request.user
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["form"] = kwargs.get(
            "form",
            UserAddressForm()
        )

        return context

    def post(self, request, *args, **kwargs):
        form = UserAddressForm(request.POST)

        if form.is_valid():
            address = form.save(commit=False)

            address.user = request.user

            address.save()

            messages.success(
                request,
                "آدرس شما با موفقیت ثبت شد."
            )

            return redirect("dashboard:address-list")

        self.object_list = self.get_queryset()

        context = self.get_context_data(form=form)

        return self.render_to_response(context)


class AddressUpdateView(LoginRequiredMixin, UpdateView):

    model = UserAddressModel
    form_class = UserAddressForm

    template_name = "dashboard/user-address-edit.html"

    success_url = reverse_lazy(
        "dashboard:address-list"
    )

    login_url = "accounts:login"

    def get_queryset(self):
        return UserAddressModel.objects.filter(
            user=self.request.user
        )

    def form_valid(self, form):

        response = super().form_valid(form)

        messages.success(
            self.request,
            "آدرس شما با موفقیت ویرایش شد."
        )

        return response

    def form_invalid(self, form):
        return super().form_invalid(form)


class AddressDeleteView(LoginRequiredMixin, View):
    login_url = "accounts:login"

    def post(self, request, pk, *args, **kwargs):
        address = get_object_or_404(
            UserAddressModel,
            pk=pk,
            user=request.user
        )

        address.delete()

        messages.success(
            request,
            "آدرس با موفقیت حذف شد."
        )

        return redirect("dashboard:address-list")


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):

    model = Profile
    form_class = UserProfileForm

    template_name = "dashboard/user-profile.html"

    success_url = reverse_lazy(
        "dashboard:user-profile"
    )

    login_url = "accounts:login"

    def get_object(self, queryset=None):
        return self.request.user.user_profile

    def form_valid(self, form):

        response = super().form_valid(form)

        messages.success(
            self.request,
            "اطلاعات پروفایل شما با موفقیت ویرایش شد."
        )

        return response

    def form_invalid(self, form):

        messages.error(
            self.request,
            "اطلاعات وارد شده صحیح نیست. لطفاً فرم را بررسی کنید."
        )

        return super().form_invalid(form)

from django import forms
from .models import UserAddressModel
from accounts.models import Profile


class UserAddressForm(forms.ModelForm):

    class Meta:
        model = UserAddressModel

        fields = [
            "first_name",
            "last_name",
            "state",
            "city",
            "postal_code",
            "phone_number",
            "address",
            "description",
        ]

        labels = {
            "first_name": "نام",
            "last_name": "نام خانوادگی",
            "state": "استان",
            "city": "شهر",
            "postal_code": "کد پستی",
            "phone_number": "شماره تلفن",
            "address": "آدرس",
            "description": "توضیحات",
        }

        error_messages = {
            "first_name": {
                "required": "لطفاً نام خود را وارد کنید.",
                "max_length": "نام نمی‌تواند بیشتر از ۵۰ کاراکتر باشد.",
            },
            "last_name": {
                "required": "لطفاً نام خانوادگی خود را وارد کنید.",
                "max_length": "نام خانوادگی نمی‌تواند بیشتر از ۵۰ کاراکتر باشد.",
            },
            "state": {
                "required": "لطفاً استان را وارد کنید.",
                "max_length": "نام استان نمی‌تواند بیشتر از ۵۰ کاراکتر باشد.",
            },
            "city": {
                "required": "لطفاً شهر را وارد کنید.",
                "max_length": "نام شهر نمی‌تواند بیشتر از ۵۰ کاراکتر باشد.",
            },
            "postal_code": {
                "required": "لطفاً کد پستی را وارد کنید.",
                "max_length": "کد پستی معتبر نیست.",
            },
            "phone_number": {
                "required": "لطفاً شماره تلفن را وارد کنید.",
                "max_length": "شماره تلفن معتبر نیست.",
            },
            "address": {
                "required": "لطفاً آدرس را وارد کنید.",
                "max_length": "آدرس نمی‌تواند بیشتر از ۲۰۰ کاراکتر باشد.",
            },
        }

        widgets = {
            "first_name": forms.TextInput(attrs={
                "placeholder": "نام",
            }),

            "last_name": forms.TextInput(attrs={
                "placeholder": "نام خانوادگی",
            }),

            "state": forms.TextInput(attrs={
                "placeholder": "استان",
            }),

            "city": forms.TextInput(attrs={
                "placeholder": "شهر",
            }),

            "postal_code": forms.TextInput(attrs={
                "placeholder": "کد پستی محل تحویل",
            }),

            "phone_number": forms.TextInput(attrs={
                "placeholder": "تلفن همراه",
            }),

            "address": forms.TextInput(attrs={
                "placeholder": "اطلاعات دقیق محل تحویل",
            }),

            "description": forms.Textarea(attrs={
                "placeholder": "نکات مهم درباره تحویل محصول",
                "rows": 7,
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["description"].required = False


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = Profile

        fields = [
            "first_name",
            "last_name",
            "phone_number",
        ]

        labels = {
            "first_name": "نام",
            "last_name": "نام خانوادگی",
            "phone_number": "شماره موبایل",
        }

        error_messages = {
            "first_name": {
                "required": "وارد کردن نام الزامی است.",
                "max_length": "نام نمی‌تواند بیشتر از ۲۵۵ کاراکتر باشد.",
            },
            "last_name": {
                "required": "وارد کردن نام خانوادگی الزامی است.",
                "max_length": "نام خانوادگی نمی‌تواند بیشتر از ۲۵۵ کاراکتر باشد.",
            },
            "phone_number": {
                "required": "وارد کردن شماره موبایل الزامی است.",
                "max_length": "شماره موبایل صحیح نیست.",
            },
        }

        widgets = {
            "first_name": forms.TextInput(
                attrs={
                    "class": "rounded-2xl rounded-tr-sm text-sm text-zinc-600 w-full bg-[#f0f0f0] px-5 py-3.5 placeholder:text-zinc-400 focus:outline-1 focus:outline-zinc-300",
                    "placeholder": "نام",
                }
            ),

            "last_name": forms.TextInput(
                attrs={
                    "class": "rounded-2xl rounded-tr-sm text-sm text-zinc-600 w-full bg-[#f0f0f0] px-5 py-3.5 placeholder:text-zinc-400 focus:outline-1 focus:outline-zinc-300",
                    "placeholder": "نام خانوادگی",
                }
            ),

            "phone_number": forms.TextInput(
                attrs={
                    "class": "rounded-2xl rounded-tr-sm text-sm text-zinc-600 w-full bg-[#f0f0f0] px-5 py-3.5 placeholder:text-zinc-400 focus:outline-1 focus:outline-zinc-300",
                    "placeholder": "شماره موبایل",
                    "dir": "ltr",
                }
            ),
        }

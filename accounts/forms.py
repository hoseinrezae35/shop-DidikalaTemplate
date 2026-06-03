from django import forms
from django.contrib.auth.forms import AuthenticationForm
from accounts.models import User
from django.core.exceptions import ValidationError


class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label='ایمیل', widget=forms.EmailInput(attrs={
        'class': 'rounded-xl bg-[#f0f0f0] pl-10 pr-4 py-2.5 w-full',
        'placeholder': 'example@gmail.com'
    }))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.error_messages['invalid_login'] = 'ایمیل یا رمز عبور اشتباه است. لطفاً دوباره تلاش کنید.'
        self.error_messages['inactive'] = 'حساب کاربری شما غیرفعال شده است. لطفاً با پشتیبانی تماس بگیرید.'

    def clean_username(self):
        email = self.cleaned_data.get('username')
        try:
            user = User.objects.get(email=email)
            return user.email
        except User.DoesNotExist:
            raise ValidationError('ایمیل وارد شده ثبت نام نشده است')


class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        label='رمز عبور',
        widget=forms.PasswordInput(attrs={
            'class': 'rounded-xl bg-[#f0f0f0] px-4 py-2.5 w-full',
            'placeholder': '••••••••'
        })
    )
    password_confirm = forms.CharField(
        label='تکرار رمز عبور',
        widget=forms.PasswordInput(attrs={
            'class': 'rounded-xl bg-[#f0f0f0] px-4 py-2.5 w-full',
            'placeholder': '••••••••'
        })
    )

    class Meta:
        model = User
        fields = ["email", "password"]
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'rounded-xl bg-[#f0f0f0] px-4 py-2.5 w-full',
                'placeholder': 'example@gmail.com'
            })
        }

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError("این ایمیل قبلاً ثبت شده است")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise ValidationError("رمز عبور با تکرار آن مطابقت ندارد")

        return cleaned_data


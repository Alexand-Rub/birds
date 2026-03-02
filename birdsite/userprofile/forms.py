from pyclbr import Class

from django.contrib.auth.forms import UserCreationForm, forms
from .models import Profile


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повторите', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = "first_name", "last_name", "email", "logo", "first_name"
        widgets = {
            "first_name": forms.TextInput(attrs={'class': 'profile_update-inp ',  }),
            "last_name": forms.TextInput(attrs={'class': 'profile_update-inp '}),
            "email": forms.EmailInput(attrs={'class': 'profile_update-inp '}),
            "logo": forms.FileInput(attrs={'class': 'profile_update-btn'}),
        }
        labels = {
            "first_name": 'Имя',
            "last_name": 'Фамилия',
            "email": 'e-mail',
            "logo": 'Аватарка',
        }
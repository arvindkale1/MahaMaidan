from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15, required=False)
    role = forms.ChoiceField(choices=User.Role.choices, initial=User.Role.CUSTOMER)

    class Meta:
        model = User
        fields = ('username', 'email', 'phone_number', 'role', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.phone_number = self.cleaned_data.get('phone_number', '')
        user.role = self.cleaned_data['role']
        if commit:
            user.save()
        return user

# forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser

class SignUpForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    
    class Meta:
        model = CustomUser
        fields = ['email', 'age', 'contact_number']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class SignInForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'password']

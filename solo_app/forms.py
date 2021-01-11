from django import forms
from .models import User

class RegForm(forms.ModelForm):
    password = forms.CharField(max_length=100, widget=forms.PasswordInput)
    confirm_pw = forms.CharField(max_length=100, widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = '__all__'

class LogForm(forms.ModelForm):
    password = forms.CharField(max_length=100, widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ('email', 'password')


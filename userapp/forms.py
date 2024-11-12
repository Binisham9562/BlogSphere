from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm
from django.contrib.auth.models import User
from .models import Profile

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30)
    last_name= forms.CharField(max_length=30)
    
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email', 'password1', 'password2']

class CustomLoginForm(AuthenticationForm):
    pass  # You can customize the login form here if needed

class CustomPasswordResetForm(PasswordResetForm):
    pass  # You can customize the password reset form here if needed

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture']

        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write something about yourself...'}),
        }
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class UserRegisterForm(UserCreationForm):
    """
    Form for the user signup page.
    """
    email = forms.EmailField()

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password1', 'password2', ]


class UserUpdateForm(forms.ModelForm):
    """
    Form for the user to update the username and email fields.
    """
    email = forms.EmailField()

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', ]


class ProfileUpdateForm(forms.ModelForm):
    """
    Form for the user to update the profile picture.
    """
    class Meta:
        model = Profile
        fields = ['image']

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

from .models import Donation


class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = '__all__'

class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "password"]

class UserSignUpForm(UserCreationForm):
    """User registration form."""

    first_name = forms.CharField(
        label="First name",
        max_length=100,
        required=True,
        ),
    

    last_name = forms.CharField(
        label="Last name",
        max_length=100,
        required=True,
         ),
    

    email = forms.EmailField(
        label="Email address",
        max_length=254,
        required=True,
        ),
    

    password1 = forms.CharField(
        label="Password",
        help_text="<ul class='errorlist text-muted'><li>Your password can 't be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can 't be a commonly used password.</li> <li>Your password can 't be entirely numeric.</ul>",
        max_length=100,
        required=True,
        ),
    

    password2 = forms.CharField(
        label="Confirm password",
        help_text=False,
        max_length=100,
        required=True,
    )

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )

    def clean(self):
        cleaned_data = super(UserSignUpForm, self).clean()
        password = cleaned_data.get('password1')
        password_confirm = cleaned_data.get('password2')

        if password and password_confirm:
            if password != password_confirm:
                msg = "The two password fields must match."
                self.add_error('password_confirm', msg)
        return cleaned_data
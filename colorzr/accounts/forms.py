from django import forms
from django.contrib.auth.forms import *
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    # Extra controls
    first_name = forms.CharField(
        max_length=30,
        required=False,
        help_text='Optional.'
    )
    last_name = forms.CharField(
        max_length=30,
        required=False,
        help_text='Optional.'
    )
    email = forms.EmailField(
        max_length=254,
        help_text='Required. Inform a valid email address.'
    )

    # Fix to style the default controls
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs['class'] = 'form-control'

        # Add any overrides here

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        )


class LoginForm(AuthenticationForm):
    # Fix to style the default controls
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs['class'] = 'form-control'

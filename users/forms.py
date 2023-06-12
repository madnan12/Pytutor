from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm

User_Type = [
    ('Teacher', 'Teacher'),
    ('Student', 'Student'),
]

class CreateUserForm(UserCreationForm):
    user_type = forms.ChoiceField(required=True, choices=User_Type, widget=forms.RadioSelect)
    email = forms.EmailField(max_length=254, required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_type'].widget.attrs.update({'class': 'custom-control-input'})

    class Meta:
        model = CustomUser
        fields = ("username", "email", "password1", "password2", "user_type")

class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(label='First Name', required=True, max_length=100)
    last_name = forms.CharField(label='Last Name', required=True, max_length=100)
    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'placeholder': 'First name', 'class': 'form-control',})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Last name', 'class': 'form-control',})
        self.fields['email'].widget.attrs.update({'placeholder': 'Email', 'class': 'form-control',})

    class Meta:
        model = CustomUser
        fields = [  
            'first_name',
            'last_name',
            'email',
        ]

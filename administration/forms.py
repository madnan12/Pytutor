from django import forms
from users.models import CustomUser
from .models import Subject

User_Type = [
    ('Teacher', 'Teacher'),
    ('Student', 'Student'),
]

class UserForm(forms.ModelForm):
    first_name = forms.CharField(label='First Name', required=True, max_length=100)
    last_name = forms.CharField(label='Last Name', required=True, max_length=100)
    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'placeholder': 'First name', 'class': 'form-control',})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Last name', 'class': 'form-control',})
        self.fields['email'].widget.attrs.update({'placeholder': 'Email', 'class': 'form-control',})
        self.fields['is_active'].widget.attrs.update({'class': 'custom-control-input',})
        self.fields['user_type'].widget.attrs.update({'placeholder': 'Email', 'class': 'form-control form-select',})


    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'user_type', 'is_active']

class SubjectForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'placeholder': 'Title', 'class': 'form-control',})
        self.fields['description'].widget.attrs.update({'class': 'form-control',})

    def clean(self):
        cleaned_date = super().clean()
        title =  cleaned_date.get('title',None)
        description = cleaned_date.get('description',None)
        description_character_count = len(str(description))

        if not title:
            self.add_error('title','Please provide title for this subject')

        if description and description_character_count < 100:
            self.add_error('description', f'Description should be of atleat 100 characters. You provided only {description_character_count} characters')

        elif not description:
            self.add_error('description', f'Please provide description for this subject')

    class Meta:
        model = Subject
        fields = ['title', 'description']
        labels = {
            'title'     : 'Subject Title',
            'description'  : 'Subject Description'
        }

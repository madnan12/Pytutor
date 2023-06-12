from django import forms
from students_portal.models import Answer
from users.models import CustomUser
from .models import Course, Topic
from administration.models import Subject

class CourseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'placeholder': 'Title', 'class': 'form-control',})
        self.fields['subject'].queryset = Subject.objects.all()
        self.fields['subject'].widget.attrs.update({'class': 'form-control form-select'})
        self.fields['description'].widget.attrs.update({'class': 'form-control',})

    def clean(self):
        cleaned_date = super().clean()
        title =  cleaned_date.get('title',None)
        description = cleaned_date.get('description',None)
        description_character_count = len(str(description))

        if not title:
            self.add_error('title','Please provide title for this course')

        if description and description_character_count < 100:
            self.add_error('description', f'Description should be of atleat 100 characters. You provided only {description_character_count} characters')

        elif not description:
            self.add_error('description', f'Please provide description for this course')

    class Meta:
        model = Course
        fields = ['title', 'subject', 'description']
        labels = {
            'title'     : 'Course Title',
            'description'  : 'Course Description'
        }

class TopicForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'placeholder': 'Title', 'class': 'form-control',})
        self.fields['course'].queryset = Course.objects.all()
        self.fields['course'].widget.attrs.update({'class': 'form-control form-select'})
        self.fields['description'].widget.attrs.update({'class': 'form-control',})

    def clean(self):
        cleaned_date = super().clean()
        title =  cleaned_date.get('title',None)
        description = cleaned_date.get('description',None)
        description_character_count = len(str(description))

        if not title:
            self.add_error('title','Please provide title for this topic')

        if description and description_character_count < 100:
            self.add_error('description', f'Description should be of atleat 100 characters. You provided only {description_character_count} characters')

        elif not description:
            self.add_error('description', f'Please provide description for this topic')

    class Meta:
        model = Topic
        fields = ['title', 'course', 'description']
        labels = {
            'title'     : 'Topic Title',
            'description'  : 'Topic Description'
        }

class AnswerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['explanation'].widget.attrs.update({'class': 'form-control'})
        self.fields['answer_text'].widget.attrs.update({'class': 'form-control'})
        self.fields['answer_text'].disabled = True
        self.fields['question'].widget.attrs.update({'class': 'form-control'})
        self.fields['question'].disabled = True
        

    class Meta:
        model = Answer
        fields = ['question','answer_text', 'is_correct', 'explanation',]
        labels = {
            'explanation': 'Explanation',
            'question': 'Question',
            'answer_text': 'Answer',
        }
        


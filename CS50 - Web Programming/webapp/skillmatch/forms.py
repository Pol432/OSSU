from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from .models import Project


class EditProject(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
        widgets = {
            'careers': forms.CheckboxSelectMultiple(attrs={'class': 'select-multiple'}),
            'abilities': forms.CheckboxSelectMultiple(attrs={'class': 'select-multiple'}),
        }


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'introduction', 'instructions', 'courses', 'image', "careers", "abilities"]
        widgets = {
            'careers': forms.CheckboxSelectMultiple(attrs={'class': 'select-multiple'}),
            'abilities': forms.CheckboxSelectMultiple(attrs={'class': 'select-multiple'}),
        }
        labels = {
            'introduction': 'Introduction (Use Markdown Language)',
            'instructions': 'Instructions (Use Markdown Language)',
            'courses': 'Courses (Use Markdown Language)',
        }

    def save(self, commit=True):
        project = super().save(commit=False)
        project.pending = True
        
        if commit:
            project.save()
            self.save_m2m()  # Save many-to-many fields
        
        return project




class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label="Username")
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label="Password")

User = get_user_model()

class SignupForm(UserCreationForm):
    user_type = forms.MultipleChoiceField(
        required=True,
        widget=forms.CheckboxSelectMultiple,
        choices=(('student', 'Student'), ('teacher', 'Teacher')),
        label=('User Type')
    )
    username = forms.CharField(help_text='', label="Username", max_length=70)
    password1 = forms.CharField(help_text='', widget=forms.PasswordInput, label="Password", max_length=9)
    password2 = forms.CharField(help_text='', widget=forms.PasswordInput, label="Password confirmation", max_length=9)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'user_type')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = self.cleaned_data['user_type']

        if commit:
            user.save()
        return user

# blog/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Post

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Required. Provide a valid email address.')
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class ProfileForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)
    class Meta:
        model = Profile
        fields = ("bio", "avatar")
    def __init__(self, *args, **kwargs):
        profile_instance = kwargs.get('instance', None)
        super().__init__(*args, **kwargs)
        if profile_instance:
            self.fields['username'].initial = profile_instance.user.username
            self.fields['email'].initial = profile_instance.user.email
    def save(self, commit=True):
        profile = super().save(commit=False)
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        if username:
            profile.user.username = username
        if email:
            profile.user.email = email
        if commit:
            profile.user.save()
            profile.save()
        return profile

# --- Post form used for Create/Update ---
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']  # author & published_date handled automatically
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Post title', 'maxlength': 200}),
            'content': forms.Textarea(attrs={'rows': 10, 'placeholder': 'Write your post here...'}),
        }
    def clean_title(self):
        title = self.cleaned_data.get('title', '').strip()
        if not title:
            raise forms.ValidationError("Title cannot be empty.")
        return title


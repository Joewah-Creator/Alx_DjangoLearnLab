# blog/forms.py
from django import forms
from .models import Post, Tag  
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile, Post, Comment, Tag

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

class PostForm(forms.ModelForm):
    tags_field = forms.CharField(
        required=False,
        help_text='Add tags separated by commas (e.g. django,python,web)',
        widget=forms.TextInput(attrs={'placeholder': 'tag1, tag2, tag3'})
    )

    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Post title', 'maxlength': 200}),
            'content': forms.Textarea(attrs={'rows': 10, 'placeholder': 'Write your post here...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # prefill tags_field using taggit's tags list
        if self.instance and self.instance.pk:
            tag_names = ', '.join([t.name for t in self.instance.tags.all()])
            self.fields['tags_field'].initial = tag_names

    def clean_title(self):
        title = self.cleaned_data.get('title', '').strip()
        if not title:
            raise forms.ValidationError("Title cannot be empty.")
        return title

    def save(self, commit=True, author=None):
        """
        Save post and assign tags using django-taggit.
        Pass author when creating a new Post (CreateView will supply it).
        """
        post = super().save(commit=False)
        if author and not post.pk:
            post.author = author
        if commit:
            post.save()
            # tags_field is comma separated, assign to taggit
            tags_raw = self.cleaned_data.get('tags_field', '')
            names = [n.strip() for n in tags_raw.split(',') if n.strip()]
            # taggit supports setting a list of tag names:
            post.tags.set(*[names]) if False else post.tags.set(names)
            post.save()
        return post

class CommentForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Leave a comment...'}),
        max_length=2000,
        label=''
    )

    class Meta:
        model = Comment
        fields = ['content']

    def clean_content(self):
        content = self.cleaned_data.get('content', '').strip()
        if not content:
            raise forms.ValidationError("Comment cannot be empty.")
        return content

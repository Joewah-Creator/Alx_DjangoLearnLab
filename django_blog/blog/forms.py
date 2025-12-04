from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

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
        # Expect 'instance' to be Profile instance; we expose user fields separately
        profile_instance = kwargs.get('instance', None)
        super().__init__(*args, **kwargs)
        if profile_instance:
            self.fields['username'].initial = profile_instance.user.username
            self.fields['email'].initial = profile_instance.user.email

    def save(self, commit=True):
        profile = super().save(commit=False)
        # update related user fields
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

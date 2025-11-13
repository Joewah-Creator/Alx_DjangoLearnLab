# django-models/relationship_app/models.py

from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

# Use get_user_model for the signal sender
UserModel = get_user_model()


class Author(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')

    def __str__(self):
        return self.title

    class Meta:
        # custom permissions requested by the task
        permissions = (
            ('can_add_book', 'Can add book'),
            ('can_change_book', 'Can change book'),
            ('can_delete_book', 'Can delete book'),
        )


class Library(models.Model):
    name = models.CharField(max_length=255)
    books = models.ManyToManyField(Book, related_name='libraries', blank=True)

    def __str__(self):
        return self.name


class Librarian(models.Model):
    name = models.CharField(max_length=255)
    library = models.OneToOneField(Library, on_delete=models.CASCADE, related_name='librarian')

    def __str__(self):
        return f"{self.name} ({self.library.name})"


# -----------------------
# UserProfile (RBAC)
# -----------------------
class UserProfile(models.Model):
    ROLE_ADMIN = 'Admin'
    ROLE_LIBRARIAN = 'Librarian'
    ROLE_MEMBER = 'Member'

    ROLE_CHOICES = [
        (ROLE_ADMIN, 'Admin'),
        (ROLE_LIBRARIAN, 'Librarian'),
        (ROLE_MEMBER, 'Member'),
    ]

    # use settings.AUTH_USER_MODEL so relations point to the swapped user model
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='userprofile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_MEMBER)

    def __str__(self):
        return f"{self.user.username} ({self.role})"


# Signal: create UserProfile when a new User is created
@receiver(post_save, sender=UserModel)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

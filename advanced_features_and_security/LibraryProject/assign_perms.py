from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from relationship_app.models import Book
import sys

username = 'admin'  # change this

try:
    user = User.objects.get(username=username)
except User.DoesNotExist:
    print(f"User '{username}' not found.")
    sys.exit(1)

content_type = ContentType.objects.get_for_model(Book)
perm_add = Permission.objects.get(codename='can_add_book', content_type=content_type)
perm_change = Permission.objects.get(codename='can_change_book', content_type=content_type)
perm_delete = Permission.objects.get(codename='can_delete_book', content_type=content_type)

user.user_permissions.add(perm_add, perm_change, perm_delete)
user.save()
print("Permissions successfully assigned to:", user.username)

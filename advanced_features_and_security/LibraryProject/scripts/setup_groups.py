from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from bookshelf.models import Book

# Create groups
editors, _ = Group.objects.get_or_create(name='Editors')
viewers, _ = Group.objects.get_or_create(name='Viewers')
admins, _ = Group.objects.get_or_create(name='Admins')

# Load permissions for Book
ct = ContentType.objects.get_for_model(Book)

permissions_to_assign = {
    'can_view': Permission.objects.get(codename='can_view', content_type=ct),
    'can_create': Permission.objects.get(codename='can_create', content_type=ct),
    'can_edit': Permission.objects.get(codename='can_edit', content_type=ct),
    'can_delete': Permission.objects.get(codename='can_delete', content_type=ct),
}

# Assign permissions
# Viewers
viewers.permissions.add(permissions_to_assign['can_view'])

# Editors
editors.permissions.add(permissions_to_assign['can_view'])
editors.permissions.add(permissions_to_assign['can_create'])
editors.permissions.add(permissions_to_assign['can_edit'])

# Admins: all permissions
for perm in permissions_to_assign.values():
    admins.permissions.add(perm)

print("Groups and permissions configured successfully.")

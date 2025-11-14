# Permissions & Groups Setup (Bookshelf App Only)

## Custom Permissions
The Book model in `bookshelf/models.py` defines these custom permissions:

- can_view
- can_create
- can_edit
- can_delete

## Groups
Run this script to create groups:

    python manage.py shell < scripts/setup_groups.py

Groups created:

- Viewers → can_view
- Editors → can_view, can_create, can_edit
- Admins → all permissions

## Views Enforcement
The following views in `bookshelf/views.py` require permissions:

- protected_list_books → bookshelf.can_view
- add_book → bookshelf.can_create
- edit_book → bookshelf.can_edit
- delete_book → bookshelf.can_delete

## Testing
1. Create users in Django admin.
2. Assign each user to a specific group.
3. Try to access:
   - /bookshelf/books/
   - /bookshelf/books/add/
   - /bookshelf/books/<id>/edit/
   - /bookshelf/books/<id>/delete/
4. Permissions will be enforced automatically.

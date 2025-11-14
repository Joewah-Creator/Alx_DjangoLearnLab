from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('bookshelf/', include('bookshelf.urls')),
]



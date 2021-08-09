from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.api.urls', 'accounts_api')),
    path('api/passwords/', include('password.api.urls', 'password_api')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

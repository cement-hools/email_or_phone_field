from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from user_stat import settings

urlpatterns = [
    path('', include('user.urls')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT
    )

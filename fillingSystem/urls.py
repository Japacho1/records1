from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from files import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('', include('files.urls')),  # keep files app URLs at root
]

# Serve static & media files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

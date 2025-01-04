import app.urls
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core.views import example_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(app.urls)),
    path('main-page/', example_view, name='main_page'),  # URL to access the HTML file
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                        document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                        document_root=settings.MEDIA_ROOT)
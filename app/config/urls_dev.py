from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from .urls import urlpatterns

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [path('__debug__/', include(debug_toolbar.urls))] + \
        static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + \
        urlpatterns

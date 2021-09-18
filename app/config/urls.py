from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import TemplateView

urlpatterns = [
    path('', include('blog.urls')),
    path('admin/', admin.site.urls),
    path('error', TemplateView.as_view(template_name='error.html')),
]

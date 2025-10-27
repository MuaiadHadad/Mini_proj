"""
Configuração de URLs do projeto mini_project.
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.http import HttpResponse
import base64

# View simples para servir um favicon 1x1 transparente (image/png)
# Evita 404 quando o navegador requisita /favicon.ico
_DEF_FAVICON_B64 = (
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8Xw8AAn0B9U0iWmIAAAAASUVORK5CYII="
)

def favicon_view(_request):
    return HttpResponse(base64.b64decode(_DEF_FAVICON_B64), content_type='image/png')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('sentiment.urls')),
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('favicon.ico', favicon_view, name='favicon'),
]

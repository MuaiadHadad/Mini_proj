"""
Configuração do Django Admin para o app de análise de sentimentos.
"""
from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    Configuração do admin para o modelo Post.
    """
    list_display = ['id', 'author', 'sentiment', 'created_at']
    list_filter = ['sentiment', 'created_at']
    search_fields = ['author', 'content']
    readonly_fields = ['sentiment', 'created_at', 'updated_at']
    ordering = ['-created_at']

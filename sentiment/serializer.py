"""
Serializers para o app de análise de sentimentos.
"""
from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo Post.

    Converte objetos Post para JSON e vice-versa.
    O campo 'sentiment' é somente leitura pois é gerado automaticamente.
    """
    class Meta:
        model = Post
        fields = ['id', 'author', 'content', 'sentiment', 'created_at', 'updated_at']
        read_only_fields = ['sentiment', 'created_at', 'updated_at']


class AnalyzeTextSerializer(serializers.Serializer):
    """
    Serializer para análise de texto sem salvar no banco.
    """
    text = serializers.CharField(required=True, allow_blank=False)

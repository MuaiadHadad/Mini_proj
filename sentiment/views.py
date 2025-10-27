"""
Views da API REST para análise de sentimento.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Post
from .serializer import PostSerializer, AnalyzeTextSerializer
from .model import predict_sentiment


class PostViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar Posts.

    Fornece operações CRUD completas (Create, Read, Update, Delete).
    Automaticamente analisa o sentimento ao criar/atualizar posts.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # Desabilita paginação para que a listagem retorne uma lista simples (conforme esperado nos testes)
    pagination_class = None

    def perform_create(self, serializer):
        """
        Cria um novo post e analisa seu sentimento automaticamente.
        """
        content = self.request.data.get('content', '')
        sentiment = predict_sentiment(content)
        serializer.save(sentiment=sentiment)

    def perform_update(self, serializer):
        """
        Atualiza um post e re-analisa seu sentimento se o conteúdo mudou.
        """
        content = self.request.data.get('content', '')
        sentiment = predict_sentiment(content)
        serializer.save(sentiment=sentiment)

    @action(detail=False, methods=['post'])
    def analyze(self, request):
        """
        Endpoint para análise de sentimento sem salvar no banco de dados.

        POST /api/posts/analyze/
        Body: {"text": "texto para analisar"}
        """
        serializer = AnalyzeTextSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        text = serializer.validated_data['text']
        sentiment = predict_sentiment(text)

        return Response({
            'text': text,
            'sentiment': sentiment
        }, status=status.HTTP_200_OK)

"""
Modelos para o app de análise de sentimentos.
"""

from django.db import models

class Post(models.Model):
    """
    Modelo para armazenar posts com análise de sentimento.

    Atributos:
        author: Autor do post
        content: Conteúdo do post a ser analisado
        sentiment: Sentimento detectado (positivo/negativo/neutro)
        created_at: Data e hora de criação
        updated_at: Data e hora da última atualização
    """
    SENTIMENT_CHOICES = [
        ('positive', 'Positive'),
        ('negative', 'Negative'),
        ('neutral', 'Neutral'),
    ]

    author = models.CharField(max_length=200, verbose_name="Autor")
    content = models.TextField(verbose_name="Conteúdo")
    sentiment = models.CharField(
        max_length=10,
        choices=SENTIMENT_CHOICES,
        verbose_name="Sentimento"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    def __str__(self):
        return f"{self.author} - {self.sentiment}"

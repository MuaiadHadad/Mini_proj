"""
Testes para o app de análise de sentimentos.
"""
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Post
from .model import predict_sentiment


class PostModelTest(TestCase):
    """Testes para o modelo Post."""

    def test_create_post(self):
        """Testa a criação de um post."""
        post = Post.objects.create(
            author="Test Author",
            content="This is a test post.",
            sentiment="positive"
        )
        self.assertEqual(post.author, "Test Author")
        self.assertEqual(post.sentiment, "positive")
        self.assertIsNotNone(post.created_at)
        self.assertIsNotNone(post.updated_at)


class SentimentAnalysisTest(TestCase):
    """Testes para a análise de sentimento."""

    def test_positive_sentiment(self):
        """Testa detecção de sentimento positivo."""
        result = predict_sentiment("I love this! It's amazing and wonderful!")
        self.assertEqual(result, "positive")

    def test_negative_sentiment(self):
        """Testa detecção de sentimento negativo."""
        result = predict_sentiment("I hate this. It's terrible and awful.")
        self.assertEqual(result, "negative")

    def test_neutral_sentiment(self):
        """Testa detecção de sentimento neutro."""
        result = predict_sentiment("This is a statement.")
        self.assertIn(result, ["neutral", "positive", "negative"])

    def test_empty_text(self):
        """Testa texto vazio."""
        result = predict_sentiment("")
        self.assertEqual(result, "neutral")


class PostAPITest(APITestCase):
    """Testes para a API de Posts."""

    def setUp(self):
        """Configuração inicial para os testes."""
        self.post_data = {
            "author": "Test Author",
            "content": "This is a great test!"
        }

    def test_create_post(self):
        """Testa criação de post via API."""
        response = self.client.post('/api/posts/', self.post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(response.data['author'], "Test Author")
        self.assertIn('sentiment', response.data)

    def test_list_posts(self):
        """Testa listagem de posts."""
        # Cria 2 posts de teste
        post1 = Post.objects.create(author="Author 1", content="Content 1", sentiment="positive")
        post2 = Post.objects.create(author="Author 2", content="Content 2", sentiment="negative")

        response = self.client.get('/api/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Verifica que há pelo menos 2 posts
        self.assertGreaterEqual(len(response.data), 2)

        # Verifica que os posts criados estão na resposta
        post_ids = [post['id'] for post in response.data]
        self.assertIn(post1.id, post_ids)
        self.assertIn(post2.id, post_ids)

    def test_analyze_endpoint(self):
        """Testa endpoint de análise rápida."""
        data = {"text": "I love this product!"}
        response = self.client.post('/api/posts/analyze/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('sentiment', response.data)
        self.assertIn('text', response.data)

    def test_analyze_endpoint_empty_text(self):
        """Testa análise com texto vazio."""
        data = {"text": ""}
        response = self.client.post('/api/posts/analyze/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

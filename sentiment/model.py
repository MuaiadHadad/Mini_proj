"""
Modelo de Machine Learning para análise de sentimentos.

Este módulo contém um classificador de sentimentos simples baseado em Naive Bayes.
Em produção, considere usar modelos mais sofisticados ou APIs de NLP.
"""

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from textblob import TextBlob

# Dados de treinamento mínimos (exemplo para demonstração)
# Em produção, use um dataset maior e mais robusto
texts = [
    "I love Django", "This project is awesome", "Great work", "Excellent job",
    "I hate bugs", "This code is terrible", "Very bad", "Poor quality",
    "Adoro programar", "Excelente projeto", "Muito bom",
    "Odeio erros", "Código ruim", "Péssimo"
]
labels = [
    "positive", "positive", "positive", "positive",
    "negative", "negative", "negative", "negative",
    "positive", "positive", "positive",
    "negative", "negative", "negative"
]

# Inicialização do vetorizador e do classificador
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(texts)
clf = MultinomialNB()
clf.fit(X, labels)

def predict_sentiment(text):
    """
    Analisa o sentimento de um texto usando TextBlob.

    Args:
        text (str): Texto a ser analisado

    Returns:
        str: 'positive', 'negative' ou 'neutral'
    """
    if not text or not text.strip():
        return 'neutral'

    try:
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity

        if polarity > 0:
            return 'positive'
        elif polarity < 0:
            return 'negative'
        else:
            return 'neutral'
    except Exception as e:
        print(f"Erro ao analisar sentimento: {e}")
        return 'neutral'

#!/bin/sh
# Script de inicialização do Docker

# Aplicar migrações do banco de dados
echo "Aplicando migrações do banco de dados..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput

# Coletar arquivos estáticos
echo "Coletando arquivos estáticos..."
python manage.py collectstatic --noinput --clear || true

# Criar superusuário (valores podem ser sobrescritos por variáveis de ambiente)
echo "Verificando superusuário..."
python manage.py shell << 'END'
from django.contrib.auth import get_user_model
import os

User = get_user_model()
username = os.getenv('DJANGO_SUPERUSER_USERNAME', 'admin')
email = os.getenv('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
password = os.getenv('DJANGO_SUPERUSER_PASSWORD', 'admin123')

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"Superusuário criado: {username}/{password}")
else:
    print('Superusuário já existe')
END

echo "Iniciando servidor..."
exec "$@"

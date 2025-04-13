#!/bin/sh

echo "Esperando o banco iniciar..."
while ! nc -z db 5432; do
  sleep 1
done

echo "Banco pronto!"

if [ "$ENV" = "prod" ]; then
  echo "Rodando em produção com Gunicorn..."
  gunicorn control_plus.wsgi:application --bind 0.0.0.0:8000
else
  echo "Rodando em desenvolvimento com runserver..."
  python manage.py runserver 0.0.0.0:8000
fi

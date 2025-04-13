# Dockerfile
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    netcat-openbsd gcc postgresql libpq-dev && \
    apt-get clean


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY start.sh /start.sh
RUN chmod +x /start.sh

COPY default.conf /./nginx/default.conf

COPY . .

ARG ENV=dev
ENV ENV=${ENV}

# Coleta arquivos estáticos só em produção
RUN if [ "$ENV" = "prod" ]; then python manage.py collectstatic --noinput; fi

# Expõe a porta do Gunicorn
EXPOSE 8000

CMD ["/start.sh"]

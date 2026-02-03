FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Dependências Python
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Projeto
COPY . .

# Coletar arquivos estáticos
RUN python manage.py collectstatic --noinput

EXPOSE 8023

# Django direto (EasyPanel faz o resto)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8023"]

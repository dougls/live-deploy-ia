FROM python:3.10-slim

# Criar usuário não-root
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Copiar requirements.txt para otimizar o cache de layers
COPY requirements.txt requirements.txt

# Instalar dependências globalmente (sem venv)
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY . /app

# Mudar para usuário não-root
USER appuser

# Definir o diretório de trabalho
WORKDIR /app

# Expor a porta 8080
EXPOSE 8080

# Comando para executar a aplicação
CMD ["python", "app.py"]
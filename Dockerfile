FROM python:3.10-slim

# Copia o requirements.txt para otimizar o cache de layers
COPY requirements.txt .

# Instala as dependências globalmente
RUN pip install --no-cache-dir -r requirements.txt

# Cria um usuário não-root
RUN groupadd --gid 1001 appuser && useradd --uid 1001 --gid appuser --shell /bin/bash --create-home appuser

# Copia o código da aplicação
COPY app.py /app/

# Muda para o usuário não-root
USER appuser

# Define o diretório de trabalho
WORKDIR /app

# Executa a aplicação
CMD ["python", "app.py"]

# Exporta a porta 8080
EXPOSE 8080
# Imagem base leve do Python
FROM python:3.10-slim

# Define o diretório de trabalho
WORKDIR /app

# Cria um usuário não-root
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Copia o requirements.txt para otimizar o cache
COPY requirements.txt .

# Instala as dependências globalmente
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código da aplicação
COPY . .

# Muda para o usuário não-root
USER appuser

# Comando para executar a aplicação
CMD ["python", "app.py"]

# Exporta a porta 8080
EXPOSE 8080
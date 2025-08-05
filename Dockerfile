# Use uma imagem base leve
FROM python:3.10-slim

# Defina o diretório de trabalho
WORKDIR /app

# Crie um usuário não-root
RUN groupadd --gid 1001 appuser && useradd --uid 1001 --gid appuser appuser

# Copie requirements.txt para otimizar o cache de layers
COPY requirements.txt .

# Instale as dependências globalmente, sem cache
RUN pip install --no-cache-dir -r requirements.txt

# Copie o restante do código da aplicação
COPY . .

# Mude para o usuário não-root
USER appuser

# Defina o comando para executar a aplicação
CMD ["python", "app.py"]

# Exponha a porta 8080
EXPOSE 8080
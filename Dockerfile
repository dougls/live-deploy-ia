FROM python:3.10-slim

# Criar um usuário não-root
RUN groupadd --gid 1001 appuser && useradd --uid 1001 --gid appuser appuser

# Copiar requirements.txt para otimizar o cache
COPY requirements.txt .

# Instalar dependências globalmente
RUN pip install --no-cache-dir -r requirements.txt

# Mudar para o usuário appuser
USER appuser

# Copiar o código da aplicação
COPY app.py .

# Definir o diretório de trabalho
WORKDIR /app

# Expor a porta
EXPOSE 8080

# Comando para executar a aplicação
CMD ["python", "app.py"]
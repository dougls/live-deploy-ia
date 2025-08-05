FROM python:3.10-slim

# Criar usuário não-root
RUN groupadd --gid 1001 appuser && useradd --uid 1001 --gid appuser appuser

# Copiar requirements.txt para otimizar o cache de layers
COPY requirements.txt .

# Instalar dependências globalmente
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código da aplicação
COPY app.py .

# Mudar para o usuário não-root
USER appuser

# Expor a porta 8080
EXPOSE 8080

# Comando para executar a aplicação
CMD ["python", "app.py"]
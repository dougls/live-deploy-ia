FROM python:3.10-slim

# Copia requirements.txt para otimizar o cache de layers
COPY requirements.txt .

# Instala as dependências globalmente
RUN pip install --no-cache-dir -r requirements.txt

# Cria um usuário não-root
RUN groupadd --gid 1001 appuser && useradd --uid 1001 --gid appuser --shell /bin/bash --create-home appuser

# Copia o código da aplicação
COPY app.py /home/appuser/

# Muda para o usuário não-root
USER appuser

# Define o comando de execução
CMD ["python", "/home/appuser/app.py"]

# Expoe a porta 8080
EXPOSE 8080
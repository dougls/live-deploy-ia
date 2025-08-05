import os
import sys
import json
import requests
import time

# --- Configuração ---
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"
API_KEY = os.environ.get("GEMINI_API_KEY")

if not API_KEY:
    print("Erro: A variável de ambiente GEMINI_API_KEY não está definida.")
    sys.exit(1)

def get_project_context():
    """Lê os arquivos do projeto para criar um contexto para a IA."""
    try:
        with open("app.py", "r") as f:
            app_code = f.read()
        with open("requirements.txt", "r") as f:
            requirements = f.read()
        
        context = f"""
        Conteúdo de 'app.py':
        ---
        {app_code}
        ---

        Conteúdo de 'requirements.txt':
        ---
        {requirements}
        ---
        """
        return context
    except FileNotFoundError as e:
        print(f"Erro: Arquivo não encontrado - {e}")
        sys.exit(1)

def generate_dockerfile_with_ai(context):
    """
    Envia o contexto do projeto para a API do Gemini e pede para gerar um Dockerfile otimizado.
    """
    prompt = f"""
    Com base no seguinte projeto Python/Flask, gere um Dockerfile de produção otimizado e simples, sem usar um ambiente virtual (venv).

    Contexto do Projeto:
    {context}

    Requisitos para o Dockerfile:
    1.  **Imagem Base:** Use uma imagem base leve como `python:3.10-slim`.
    2.  **Sem Venv:** Não crie ou use um ambiente virtual. O contêiner é o isolamento.
    3.  **Instalação de Dependências:**
        a. Copie `requirements.txt` primeiro para otimizar o cache de layers.
        b. Instale as dependências globalmente usando `pip install --no-cache-dir -r requirements.txt`.
    4.  **Código da Aplicação:** Depois de instalar as dependências, copie o resto do código da aplicação (ex: `app.py`).
    5.  **Segurança:** Crie e mude para um usuário não-root ('appuser').
    6.  **Comando de Execução:** Use `CMD ["python", "app.py"]` para iniciar a aplicação.
    7.  **Porta:** Exponha a porta 8080.
    8.  **Comentários:** Adicione comentários explicando os passos importantes.

    Responda APENAS com o código do Dockerfile, sem nenhuma explicação extra ou formatação de markdown como ```dockerfile.
    """

    headers = {"Content-Type": "application/json"}
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    
    max_retries = 5
    backoff_factor = 2
    
    for attempt in range(max_retries):
        try:
            response = requests.post(f"{API_URL}?key={API_KEY}", headers=headers, json=payload, timeout=60)
            response.raise_for_status() # Lança exceção para códigos de erro HTTP
            
            data = response.json()
            
            if 'candidates' in data and data['candidates']:
                content = data['candidates'][0]['content']['parts'][0]['text']
                return content.strip()
            else:
                print("Resposta da API recebida, mas sem conteúdo válido.")
                print("Resposta completa:", json.dumps(data, indent=2))
                return None

        except requests.exceptions.RequestException as e:
            print(f"Erro na chamada da API (tentativa {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                sleep_time = backoff_factor ** attempt
                print(f"Aguardando {sleep_time}s para tentar novamente...")
                time.sleep(sleep_time)
            else:
                print("Número máximo de tentativas atingido. Falha ao gerar Dockerfile.")
                return None
    return None


if __name__ == "__main__":
    print("Analisando o projeto para gerar o Dockerfile...")
    project_context = get_project_context()
    
    print("Chamando a API de IA para gerar o Dockerfile...")
    dockerfile_content = generate_dockerfile_with_ai(project_context)

    if dockerfile_content:
        with open("Dockerfile", "w") as f:
            f.write(dockerfile_content)
        print("Dockerfile gerado com sucesso pela IA!")
    else:
        print("Falha ao gerar o Dockerfile. O processo será encerrado.")
        sys.exit(1)
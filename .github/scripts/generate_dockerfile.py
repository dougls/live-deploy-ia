import os
import sys
import json
import requests
import time

# --- Configuração ---
# Use a Gemini Flash API para uma resposta rápida e eficiente.
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-preview-0514:generateContent"
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
    Com base no seguinte projeto Python/Flask, gere um Dockerfile de produção otimizado.

    Contexto do Projeto:
    {context}

    Requisitos para o Dockerfile:
    1.  **Multi-stage build:** Use um estágio de 'builder' para instalar dependências e um estágio final leve.
    2.  **Imagem base leve:** Use uma imagem base slim para Python (ex: python:3.10-slim).
    3.  **Usuário não-root:** Crie e utilize um usuário não-root por segurança.
    4.  **Porta:** Exponha a porta 8080, que é a porta que a aplicação Flask está usando.
    5.  **Otimização de cache:** Copie 'requirements.txt' e instale as dependências antes de copiar o resto do código.
    6.  **Comentários:** Adicione comentários explicando cada passo importante.

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
                # Se a resposta não tiver o formato esperado, mas foi bem-sucedida (200 OK)
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
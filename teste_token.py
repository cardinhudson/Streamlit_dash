import os
import requests

# Carregar token do arquivo .env
def load_token():
    try:
        if os.path.exists('.env'):
            with open('.env', 'r', encoding='utf-8') as f:
                for line in f:
                    if line.startswith('HUGGINGFACE_TOKEN='):
                        return line.split('=')[1].strip()
    except Exception as e:
        print(f"Erro ao carregar token: {e}")
    return None

# Testar conexão
def test_connection(token):
    try:
        url = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"
        headers = {"Authorization": f"Bearer {token}"}
        
        payload = {
            "inputs": "Teste de conexão",
            "parameters": {
                "max_length": 10,
                "temperature": 0.7
            }
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        
        if response.status_code == 200:
            return True, "✅ Conexão bem-sucedida!"
        elif response.status_code == 401:
            return False, "❌ Token inválido ou expirado"
        elif response.status_code == 429:
            return False, "⚠️ Limite de requisições excedido"
        else:
            return False, f"❌ Erro na API: {response.status_code}"
            
    except requests.exceptions.Timeout:
        return False, "⏰ Timeout na conexão"
    except requests.exceptions.ConnectionError:
        return False, "🌐 Erro de conexão com a internet"
    except Exception as e:
        return False, f"❌ Erro inesperado: {str(e)}"

# Executar teste
if __name__ == "__main__":
    print("🔑 Testando token do Hugging Face...")
    
    token = load_token()
    if token:
        print(f"Token encontrado: {token[:10]}...{token[-10:]}")
        success, message = test_connection(token)
        print(message)
    else:
        print("❌ Token não encontrado no arquivo .env")


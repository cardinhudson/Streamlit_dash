import streamlit as st
import os
import requests
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="Configurar IA - KE5Z",
    page_icon="⚙️",
    layout="wide"
)

# Verificar autenticação
from auth import verificar_autenticacao, verificar_status_aprovado
verificar_autenticacao()

# Verificar se o usuário está aprovado
if 'usuario_nome' in st.session_state and not verificar_status_aprovado(st.session_state.usuario_nome):
    st.warning("⏳ Sua conta ainda está pendente de aprovação.")
    st.stop()

# Título da página
st.title("⚙️ Configuração da IA - Hugging Face")
st.markdown("---")

# Função para testar conexão
def test_connection(token):
    """Testa a conexão com a API do Hugging Face"""
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

# Função para salvar token
def save_token(token):
    """Salva o token no arquivo .env"""
    try:
        # Ler arquivo .env existente se houver
        env_content = []
        if os.path.exists('.env'):
            with open('.env', 'r', encoding='utf-8') as f:
                env_content = f.readlines()
        
        # Atualizar ou adicionar token
        token_line = f"HUGGINGFACE_TOKEN={token}\n"
        token_found = False
        
        for i, line in enumerate(env_content):
            if line.startswith('HUGGINGFACE_TOKEN='):
                env_content[i] = token_line
                token_found = True
                break
        
        if not token_found:
            env_content.append(token_line)
        
        # Salvar arquivo .env
        with open('.env', 'w', encoding='utf-8') as f:
            f.writelines(env_content)
        
        return True, "✅ Token salvo com sucesso!"
        
    except Exception as e:
        return False, f"❌ Erro ao salvar token: {str(e)}"

# Função para carregar token
def load_token():
    """Carrega o token do arquivo .env"""
    try:
        if os.path.exists('.env'):
            with open('.env', 'r', encoding='utf-8') as f:
                for line in f:
                    if line.startswith('HUGGINGFACE_TOKEN='):
                        return line.split('=')[1].strip()
    except:
        pass
    return None

# Interface principal
st.subheader("🔑 Configuração do Token")

# Carregar token atual
current_token = load_token()

if current_token:
    st.success("✅ Token já configurado!")
    st.info("🔐 Token do Hugging Face está configurado e pronto para uso")
    
    # Botão para testar conexão
    if st.button("🧪 Testar Conexão Atual"):
        with st.spinner("Testando conexão..."):
            success, message = test_connection(current_token)
            if success:
                st.success(message)
            else:
                st.error(message)
    
    # Botão para alterar token
    if st.button("🔄 Alterar Token"):
        st.session_state.show_token_input = True
        st.rerun()
else:
    st.warning("⚠️ Nenhum token configurado")
    st.session_state.show_token_input = True

# Formulário para inserir token
if st.session_state.get('show_token_input', False):
    st.markdown("---")
    st.subheader("📝 Inserir Novo Token")
    
    with st.form("token_form"):
        st.markdown("""
        **Como obter o token:**
        1. Acesse [Hugging Face](https://huggingface.co/settings/tokens)
        2. Faça login na sua conta
        3. Clique em "New token"
        4. Dê um nome ao token (ex: "KE5Z Dashboard")
        5. Selecione "Read" como permissão
        6. Copie o token gerado
        """)
        
        new_token = st.text_input(
            "Token do Hugging Face:",
            type="password",
            placeholder="hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
            help="Cole aqui o token copiado do Hugging Face"
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            submit_button = st.form_submit_button("💾 Salvar Token", use_container_width=True)
        
        with col2:
            cancel_button = st.form_submit_button("❌ Cancelar", use_container_width=True)
        
        if submit_button and new_token:
            if new_token.startswith('hf_'):
                # Salvar token
                success, message = save_token(new_token)
                if success:
                    st.success(message)
                    st.session_state.show_token_input = False
                    st.rerun()
                else:
                    st.error(message)
            else:
                st.error("❌ Token deve começar com 'hf_'")
        
        if cancel_button:
            st.session_state.show_token_input = False
            st.rerun()

# Informações sobre a API
st.markdown("---")
st.subheader("ℹ️ Sobre a API Hugging Face")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **🎯 Funcionalidades:**
    - Análise de linguagem natural
    - Interpretação de perguntas
    - Geração de respostas
    - Processamento de texto
    """)

with col2:
    st.markdown("""
    **💰 Custo:**
    - **Gratuito** para uso básico
    - Limite de requisições por hora
    - Sem necessidade de cartão de crédito
    - Ideal para projetos pessoais
    """)

# Status da configuração
st.markdown("---")
st.subheader("📊 Status da Configuração")

col1, col2, col3 = st.columns(3)

with col1:
    if current_token:
        st.success("✅ Token Configurado")
    else:
        st.error("❌ Token Não Configurado")

with col2:
    if current_token:
        st.success("✅ Arquivo .env Criado")
    else:
        st.warning("⚠️ Arquivo .env Não Encontrado")

with col3:
    if current_token:
        st.success("✅ Pronto para Uso")
    else:
        st.warning("⚠️ Configuração Necessária")

# Instruções de uso
st.markdown("---")
st.subheader("📖 Como Usar")

st.markdown("""
1. **Configure o token** usando o formulário acima
2. **Teste a conexão** para verificar se está funcionando
3. **Acesse a página "Assistente IA"** para usar o chatbot
4. **Faça perguntas** sobre seus dados em linguagem natural
5. **Visualize os resultados** em gráficos e tabelas
""")

# Troubleshooting
st.markdown("---")
st.subheader("🔧 Solução de Problemas")

with st.expander("❓ Problemas Comuns"):
    st.markdown("""
    **Token não funciona:**
    - Verifique se o token está correto
    - Confirme se tem permissões de leitura
    - Teste a conexão novamente
    
    **Erro de conexão:**
    - Verifique sua conexão com a internet
    - Aguarde alguns minutos e tente novamente
    - Verifique se a API está funcionando
    
    **Limite excedido:**
    - Aguarde 1 hora para resetar o limite
    - Considere usar um token diferente
    - Verifique seu plano no Hugging Face
    """)

# Rodapé
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>🤖 Dashboard KE5Z - Configuração IA | Powered by Hugging Face</p>
</div>
""", unsafe_allow_html=True)

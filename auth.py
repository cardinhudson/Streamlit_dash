"""
Módulo de autenticação compartilhado para todas as páginas do Streamlit
"""
import streamlit as st
import hashlib
import json
from datetime import datetime

# Função para carregar usuários do arquivo JSON


def carregar_usuarios():
    try:
        with open('usuarios.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Função para salvar usuários no arquivo JSON
def salvar_usuarios(usuarios):
    with open('usuarios.json', 'w', encoding='utf-8') as f:
        json.dump(usuarios, f, ensure_ascii=False, indent=2)

# Função para criar hash da senha
def criar_hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

# Função para verificar credenciais
def verificar_login(username, senha):
    usuarios = carregar_usuarios()
    if username in usuarios:
        senha_hash = criar_hash_senha(senha)
        return senha_hash == usuarios[username]['senha']
    return False

# Função para verificar se o usuário está aprovado
def verificar_status_aprovado(username):
    usuarios = carregar_usuarios()
    if username in usuarios:
        return usuarios[username].get('status', 'pendente') == 'aprovado'
    return False

# Função para verificar se o usuário está logado
def verificar_sessao():
    if 'usuario_logado' not in st.session_state:
        st.session_state.usuario_logado = False
    if 'usuario_nome' not in st.session_state:
        st.session_state.usuario_nome = None
    return st.session_state.usuario_logado

# Função para fazer logout
def fazer_logout():
    st.session_state.usuario_logado = False
    st.session_state.usuario_nome = None
    st.rerun()

# Função para tela de login
def tela_login():
    st.title("🔐 Login - Dashboard KE5Z")
    st.markdown("---")
    
    with st.form("login_form"):
        st.subheader("Acesso ao Sistema")
        username = st.text_input("👤 Usuário:", placeholder="Digite seu usuário")
        senha = st.text_input("🔑 Senha:", type="password", placeholder="Digite sua senha")
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            submitted = st.form_submit_button("Entrar", use_container_width=True)
        
        if submitted:
            if verificar_login(username, senha):
                # Verificar se o usuário está aprovado
                if verificar_status_aprovado(username):
                    st.session_state.usuario_logado = True
                    st.session_state.usuario_nome = username
                    st.success(f"Bem-vindo, {username}!")
                    st.rerun()
                else:
                    st.warning("⏳ Sua conta ainda está pendente de aprovação. Aguarde o administrador aprovar seu acesso.")
            else:
                st.error("❌ Usuário ou senha incorretos!")
    
    # Seção para cadastro de novos usuários
    st.markdown("---")
    st.subheader("📝 Cadastro de Usuário")
    
    with st.expander("Criar Nova Conta"):
        with st.form("cadastro_form"):
            st.write("**Criar nova conta:**")
            novo_usuario = st.text_input("Usuário:", key="cadastro_usuario")
            nova_senha = st.text_input("Senha:", type="password", key="cadastro_senha")
            confirmar_senha = st.text_input("Confirmar Senha:", type="password", key="cadastro_confirmar")
            email = st.text_input("Email (opcional):", key="cadastro_email")
            
            if st.form_submit_button("Criar Conta", use_container_width=True):
                if nova_senha == confirmar_senha and novo_usuario and nova_senha:
                    usuarios = carregar_usuarios()
                    if novo_usuario not in usuarios:
                        usuarios[novo_usuario] = {
                            'senha': criar_hash_senha(nova_senha),
                            'data_criacao': datetime.now().isoformat(),
                            'status': 'pendente',  # Status pendente até aprovação do admin
                            'email': email if email else None
                        }
                        salvar_usuarios(usuarios)
                        st.success(f"✅ Conta '{novo_usuario}' criada com sucesso! Aguarde a aprovação do administrador.")
                        st.info("📧 Você receberá uma notificação quando sua conta for aprovada.")
                    else:
                        st.error("❌ Usuário já existe!")
                else:
                    st.error("❌ Preencha todos os campos obrigatórios e confirme a senha corretamente!")

    # Seção para administrador gerenciar usuários (apenas para admin)
    st.markdown("---")
    st.subheader("👨‍💼 Área Administrativa")
    
    # Verificar se o usuário logado é admin
    if st.session_state.get('usuario_nome') == 'admin':
        # Gerenciar aprovação de usuários
        with st.expander("👥 Gerenciar Usuários Pendentes"):
            usuarios = carregar_usuarios()
            usuarios_pendentes = {k: v for k, v in usuarios.items() if v.get('status') == 'pendente'}
            
            if usuarios_pendentes:
                st.write(f"**{len(usuarios_pendentes)} usuário(s) aguardando aprovação:**")
                
                for usuario, dados in usuarios_pendentes.items():
                    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
                    
                    with col1:
                        st.write(f"👤 **{usuario}**")
                        if dados.get('email'):
                            st.write(f"📧 {dados['email']}")
                        st.write(f"📅 Criado em: {dados.get('data_criacao', 'N/A')}")
                    
                    with col2:
                        if st.button(f"✅ Aprovar", key=f"aprovar_{usuario}"):
                            usuarios[usuario]['status'] = 'aprovado'
                            usuarios[usuario]['aprovado_em'] = datetime.now().isoformat()
                            salvar_usuarios(usuarios)
                            st.success(f"✅ Usuário '{usuario}' aprovado!")
                            st.rerun()
                    
                    with col3:
                        if st.button(f"❌ Rejeitar", key=f"rejeitar_{usuario}"):
                            del usuarios[usuario]
                            salvar_usuarios(usuarios)
                            st.success(f"❌ Usuário '{usuario}' removido!")
                            st.rerun()
                    
                    with col4:
                        if st.button(f"👁️ Ver", key=f"ver_{usuario}"):
                            st.write(f"**Detalhes do usuário {usuario}:**")
                            st.json(dados)
                    
                    st.markdown("---")
            else:
                st.info("✅ Nenhum usuário pendente de aprovação.")
        
        # Listar todos os usuários com opção de exclusão
        with st.expander("📋 Gerenciar Todos os Usuários"):
            if usuarios:
                st.write("**Usuários cadastrados:**")
                
                for usuario, dados in usuarios.items():
                    col1, col2, col3 = st.columns([3, 1, 1])
                    
                    with col1:
                        status_icon = "✅" if dados.get('status') == 'aprovado' else "⏳"
                        status_text = "Aprovado" if dados.get('status') == 'aprovado' else "Pendente"
                        admin_text = " (Admin)" if usuario == 'admin' else ""
                        
                        st.write(f"{status_icon} **{usuario}**{admin_text} - {status_text}")
                        if dados.get('email'):
                            st.write(f"   📧 {dados['email']}")
                        st.write(f"   📅 Criado: {dados.get('data_criacao', 'N/A')}")
                        if dados.get('aprovado_em'):
                            st.write(f"   ✅ Aprovado: {dados.get('aprovado_em', 'N/A')}")
                    
                    with col2:
                        if usuario != 'admin':  # Admin não pode ser excluído
                            if st.button(f"🗑️ Excluir", key=f"excluir_{usuario}", type="secondary"):
                                # Confirmar exclusão
                                if st.session_state.get(f"confirmar_exclusao_{usuario}", False):
                                    # Excluir usuário
                                    del usuarios[usuario]
                                    salvar_usuarios(usuarios)
                                    st.success(f"✅ Usuário '{usuario}' excluído com sucesso!")
                                    st.rerun()
                                else:
                                    st.session_state[f"confirmar_exclusao_{usuario}"] = True
                                    st.warning(f"⚠️ Clique novamente para confirmar a exclusão de '{usuario}'")
                        else:
                            st.write("🔒 Protegido")
                    
                    with col3:
                        if st.button(f"👁️ Ver", key=f"ver_detalhes_{usuario}"):
                            st.write(f"**Detalhes do usuário {usuario}:**")
                            st.json(dados)
                    
                    st.markdown("---")
            else:
                st.info("Nenhum usuário cadastrado.")
    else:
        st.info("🔒 Apenas o administrador pode gerenciar usuários.")
        st.write("**Usuário atual:**", st.session_state.get('usuario_nome', 'Não logado'))
        
        # Seção para alterar senha (disponível para todos os usuários)
        st.markdown("---")
        st.subheader("🔑 Alterar Minha Senha")
        
        with st.expander("Alterar Senha"):
            with st.form("alterar_senha_login_form"):
                st.write("**Alterar senha de usuário:**")
                usuario_alterar = st.text_input("Usuário:", key="usuario_alterar_senha")
                senha_atual = st.text_input("Senha Atual:", type="password", key="senha_atual_login")
                nova_senha = st.text_input("Nova Senha:", type="password", key="nova_senha_login")
                confirmar_nova_senha = st.text_input("Confirmar Nova Senha:", type="password", key="confirmar_nova_senha_login")
                
                if st.form_submit_button("Alterar Senha", use_container_width=True):
                    if nova_senha == confirmar_nova_senha and nova_senha and senha_atual and usuario_alterar:
                        # Verificar se o usuário existe e a senha atual está correta
                        if verificar_login(usuario_alterar, senha_atual):
                            # Verificar se o usuário está aprovado
                            if verificar_status_aprovado(usuario_alterar):
                                # Atualizar a senha
                                usuarios = carregar_usuarios()
                                usuarios[usuario_alterar]['senha'] = criar_hash_senha(nova_senha)
                                salvar_usuarios(usuarios)
                                st.success(f"✅ Senha do usuário '{usuario_alterar}' alterada com sucesso!")
                                st.rerun()
                            else:
                                st.warning("⏳ Usuário não está aprovado. Aguarde a aprovação do administrador.")
                        else:
                            st.error("❌ Usuário ou senha atual incorretos!")
                    else:
                        st.error("❌ Preencha todos os campos e confirme a nova senha corretamente!")

# Função para criar usuário administrador inicial
def criar_admin_inicial():
    usuarios = carregar_usuarios()
    if not usuarios:  # Se não há usuários, criar admin padrão
        usuarios['admin'] = {
            'senha': criar_hash_senha('admin123'),
            'data_criacao': datetime.now().isoformat(),
            'status': 'aprovado'  # Admin sempre aprovado
        }
        salvar_usuarios(usuarios)
        st.info("👤 Usuário administrador criado: **admin** | Senha: **admin123**")
        st.warning("⚠️ **IMPORTANTE**: Altere a senha padrão após o primeiro login!")

# Função principal de autenticação - deve ser chamada no início de cada página
def verificar_autenticacao():
    """
    Função principal que deve ser chamada no início de cada página.
    Se o usuário não estiver logado, exibe a tela de login e para a execução.
    """
    # Criar usuário admin inicial se necessário
    criar_admin_inicial()
    
    # Verificar se o usuário está logado
    if not verificar_sessao():
        tela_login()
        st.stop()  # Para a execução da página se não estiver logado
    
    # Se chegou até aqui, o usuário está logado
    return True

# Função para verificar se o usuário é administrador
def eh_administrador():
    """
    Verifica se o usuário logado é o administrador.
    """
    return st.session_state.get('usuario_nome') == 'admin'

# Função para alterar senha do usuário atual
def alterar_senha_usuario():
    """
    Permite ao usuário logado alterar sua própria senha.
    """
    with st.expander("🔑 Alterar Senha"):
        with st.form("alterar_senha_form"):
            # Mostrar qual usuário está alterando a senha
            usuario_atual = st.session_state.usuario_nome
            st.write(f"**Alterar senha do usuário: {usuario_atual}**")
            
            senha_atual = st.text_input("Senha Atual:", type="password", key="senha_atual")
            nova_senha = st.text_input("Nova Senha:", type="password", key="nova_senha")
            confirmar_nova_senha = st.text_input("Confirmar Nova Senha:", type="password", key="confirmar_nova_senha")
            
            if st.form_submit_button("Alterar Senha", use_container_width=True):
                if nova_senha == confirmar_nova_senha and nova_senha and senha_atual:
                    # Verificar se a senha atual está correta
                    if verificar_login(usuario_atual, senha_atual):
                        # Atualizar a senha
                        usuarios = carregar_usuarios()
                        usuarios[usuario_atual]['senha'] = criar_hash_senha(nova_senha)
                        salvar_usuarios(usuarios)
                        st.success(f"✅ Senha do usuário '{usuario_atual}' alterada com sucesso!")
                        st.rerun()
                    else:
                        st.error("❌ Senha atual incorreta!")
                else:
                    st.error("❌ Preencha todos os campos e confirme a nova senha corretamente!")

# Função para exibir header com informações do usuário
def exibir_header_usuario():
    """
    Exibe o header com informações do usuário e botão de logout.
    Deve ser chamada após verificar_autenticacao().
    """
    col1, col2, col3 = st.columns([2, 1, 1])
    with col3:
        usuario_atual = st.session_state.usuario_nome
        if eh_administrador():
            st.write(f"👑 Admin: **{usuario_atual}**")
        else:
            st.write(f"👤 Usuário: **{usuario_atual}**")
        if st.button("🚪 Logout", type="secondary"):
            fazer_logout()

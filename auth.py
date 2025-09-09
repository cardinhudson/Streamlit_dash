#!/usr/bin/env python3
"""
Módulo de autenticação para o sistema de login
"""
import streamlit as st
import json
import hashlib
from datetime import datetime

def criar_hash_senha(senha):
    """Cria um hash SHA-256 da senha"""
    return hashlib.sha256(senha.encode()).hexdigest()

def carregar_usuarios():
    """Carrega os usuários do arquivo JSON"""
    try:
        with open('usuarios.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def salvar_usuarios(usuarios):
    """Salva os usuários no arquivo JSON"""
    with open('usuarios.json', 'w', encoding='utf-8') as f:
        json.dump(usuarios, f, indent=2, ensure_ascii=False)

def criar_admin_inicial():
    """Cria o usuário admin inicial se não existir"""
    usuarios = carregar_usuarios()
    
    if 'admin' not in usuarios:
        usuarios['admin'] = {
            'senha': criar_hash_senha('admin123'),
            'data_criacao': datetime.now().isoformat(),
            'status': 'aprovado',
            'aprovado_em': datetime.now().isoformat()
        }
        salvar_usuarios(usuarios)

def verificar_login(usuario, senha):
    """Verifica se o login é válido"""
    usuarios = carregar_usuarios()
    
    if usuario in usuarios:
        senha_hash = criar_hash_senha(senha)
        if usuarios[usuario]['senha'] == senha_hash:
            # Verificar se o usuário está aprovado
            if usuarios[usuario].get('status') == 'aprovado':
                return True
            else:
                st.error("⏳ Sua conta ainda está pendente de aprovação.")
                return False
        else:
            st.error("❌ Senha incorreta!")
            return False
    else:
        st.error("❌ Usuário não encontrado!")
        return False

def fazer_logout():
    """Faz logout do usuário"""
    if 'usuario_nome' in st.session_state:
        del st.session_state['usuario_nome']
    st.rerun()

def verificar_autenticacao():
    """Verifica se o usuário está autenticado"""
    if 'usuario_nome' not in st.session_state:
        tela_login()
        st.stop()

def verificar_status_aprovado(username):
    """Verifica se o usuário está aprovado"""
    usuarios = carregar_usuarios()
    if username in usuarios:
        return usuarios[username].get('status') == 'aprovado'
    return False

def eh_administrador():
    """Verifica se o usuário atual é administrador"""
    return st.session_state.get('usuario_nome') == 'admin'

def exibir_header_usuario():
    """Exibe o header com informações do usuário"""
    if 'usuario_nome' in st.session_state:
        st.sidebar.markdown("---")
        st.sidebar.write(f"👤 **Usuário:** {st.session_state['usuario_nome']}")
        
        if eh_administrador():
            st.sidebar.write("👑 **Administrador**")
        
        if st.sidebar.button("🚪 Logout"):
            fazer_logout()

def tela_login():
    """Exibe a tela de login"""
    st.title("🔐 Sistema de Login")
    
    # Criar admin inicial se necessário
    criar_admin_inicial()
    
    # Formulário de login
    with st.form("login_form"):
        st.subheader("📝 Fazer Login")
        usuario = st.text_input("Usuário:")
        senha = st.text_input("Senha:", type="password")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("🔓 Entrar", use_container_width=True):
                if verificar_login(usuario, senha):
                    st.session_state.usuario_nome = usuario
                    st.success(f"✅ Login realizado com sucesso! Bem-vindo, {usuario}!")
                    st.rerun()
        
        with col2:
            if st.form_submit_button("🔄 Limpar", use_container_width=True):
                st.rerun()
    
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
                            # Verificar se está alterando senha
                            if st.session_state.get(f"alterando_senha_{usuario}", False):
                                with st.form(f"form_alterar_senha_{usuario}"):
                                    st.write(f"**Alterar senha de {usuario}:**")
                                    nova_senha_admin = st.text_input("Nova Senha:", type="password", key=f"nova_senha_admin_{usuario}")
                                    confirmar_senha_admin = st.text_input("Confirmar Nova Senha:", type="password", key=f"confirmar_senha_admin_{usuario}")
                                    
                                    col_salvar, col_cancelar_senha = st.columns(2)
                                    with col_salvar:
                                        if st.form_submit_button("💾 Salvar", use_container_width=True):
                                            if nova_senha_admin == confirmar_senha_admin and nova_senha_admin:
                                                # Atualizar senha
                                                usuarios[usuario]['senha'] = criar_hash_senha(nova_senha_admin)
                                                usuarios[usuario]['alterado_por_admin_em'] = datetime.now().isoformat()
                                                salvar_usuarios(usuarios)
                                                # Limpar estado
                                                if f"alterando_senha_{usuario}" in st.session_state:
                                                    del st.session_state[f"alterando_senha_{usuario}"]
                                                st.success(f"✅ Senha de '{usuario}' alterada com sucesso!")
                                                st.rerun()
                                            else:
                                                st.error("❌ Preencha os campos e confirme a senha corretamente!")
                                    with col_cancelar_senha:
                                        if st.form_submit_button("❌ Cancelar", use_container_width=True):
                                            # Limpar estado
                                            if f"alterando_senha_{usuario}" in st.session_state:
                                                del st.session_state[f"alterando_senha_{usuario}"]
                                            st.rerun()
                            # Verificar se está confirmando exclusão
                            elif st.session_state.get(f"confirmar_exclusao_{usuario}", False):
                                col_confirmar, col_cancelar = st.columns(2)
                                with col_confirmar:
                                    if st.button(f"✅ Confirmar", key=f"confirmar_{usuario}", type="primary"):
                                        # Excluir usuário
                                        del usuarios[usuario]
                                        salvar_usuarios(usuarios)
                                        # Limpar estado de confirmação
                                        if f"confirmar_exclusao_{usuario}" in st.session_state:
                                            del st.session_state[f"confirmar_exclusao_{usuario}"]
                                        st.success(f"✅ Usuário '{usuario}' excluído com sucesso!")
                                        st.rerun()
                                with col_cancelar:
                                    if st.button(f"❌ Cancelar", key=f"cancelar_{usuario}"):
                                        # Limpar estado de confirmação
                                        if f"confirmar_exclusao_{usuario}" in st.session_state:
                                            del st.session_state[f"confirmar_exclusao_{usuario}"]
                                        st.rerun()
                                st.warning(f"⚠️ Tem certeza que deseja excluir '{usuario}'?")
                            else:
                                col_alterar, col_excluir = st.columns(2)
                                with col_alterar:
                                    if st.button(f"🔑 Alterar Senha", key=f"alterar_senha_{usuario}", type="secondary"):
                                        st.session_state[f"alterando_senha_{usuario}"] = True
                                        st.rerun()
                                with col_excluir:
                                    if st.button(f"🗑️ Excluir", key=f"excluir_{usuario}", type="secondary"):
                                        st.session_state[f"confirmar_exclusao_{usuario}"] = True
                                        st.rerun()
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
            with st.form("alterar_senha_form"):
                st.write("**Alterar senha do usuário:**")
                usuario_atual = st.text_input("Usuário:", value=st.session_state.get('usuario_nome', ''), disabled=True)
                senha_atual = st.text_input("Senha Atual:", type="password")
                nova_senha = st.text_input("Nova Senha:", type="password")
                confirmar_senha = st.text_input("Confirmar Nova Senha:", type="password")
                
                col_salvar, col_cancelar = st.columns(2)
                with col_salvar:
                    if st.form_submit_button("💾 Salvar", use_container_width=True):
                        if nova_senha == confirmar_senha and nova_senha and senha_atual:
                            usuarios = carregar_usuarios()
                            if usuario_atual in usuarios:
                                # Verificar senha atual
                                if usuarios[usuario_atual]['senha'] == criar_hash_senha(senha_atual):
                                    # Atualizar senha
                                    usuarios[usuario_atual]['senha'] = criar_hash_senha(nova_senha)
                                    usuarios[usuario_atual]['alterado_em'] = datetime.now().isoformat()
                                    salvar_usuarios(usuarios)
                                    st.success(f"✅ Senha de '{usuario_atual}' alterada com sucesso!")
                                else:
                                    st.error("❌ Senha atual incorreta!")
                            else:
                                st.error("❌ Usuário não encontrado!")
                        else:
                            st.error("❌ Preencha todos os campos e confirme a senha corretamente!")
                
                with col_cancelar:
                    if st.form_submit_button("❌ Cancelar", use_container_width=True):
                        st.rerun()
    
    # Seção de cadastro de usuário
    st.markdown("---")
    st.subheader("📝 Cadastro de Usuário")
    
    with st.expander("Cadastrar Novo Usuário"):
        with st.form("cadastro_form"):
            st.write("**Criar nova conta:**")
            novo_usuario = st.text_input("Usuário:")
            novo_email = st.text_input("Email:")
            nova_senha = st.text_input("Senha:", type="password")
            confirmar_nova_senha = st.text_input("Confirmar Senha:", type="password")
            
            col_cadastrar, col_limpar = st.columns(2)
            with col_cadastrar:
                if st.form_submit_button("📝 Cadastrar", use_container_width=True):
                    if nova_senha == confirmar_nova_senha and novo_usuario and nova_senha:
                        usuarios = carregar_usuarios()
                        if novo_usuario not in usuarios:
                            usuarios[novo_usuario] = {
                                'senha': criar_hash_senha(nova_senha),
                                'email': novo_email,
                                'data_criacao': datetime.now().isoformat(),
                                'status': 'pendente'
                            }
                            salvar_usuarios(usuarios)
                            st.success(f"✅ Usuário '{novo_usuario}' cadastrado com sucesso! Aguarde aprovação do administrador.")
                        else:
                            st.error("❌ Usuário já existe!")
                    else:
                        st.error("❌ Preencha todos os campos e confirme a senha corretamente!")
            
            with col_limpar:
                if st.form_submit_button("🔄 Limpar", use_container_width=True):
                    st.rerun()
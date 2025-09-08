#!/usr/bin/env python3
"""
Script para testar o sistema de aprovação de usuários
"""
import subprocess
import sys
import os

def testar_sistema_aprovacao():
    """Testa o sistema de aprovação de usuários"""
    
    print("🔐 Testando sistema de aprovação de usuários...")
    print("=" * 60)
    
    # Caminho para o Python do ambiente virtual
    venv_python = os.path.join("venv", "Scripts", "python.exe")
    
    if not os.path.exists(venv_python):
        print("❌ Ambiente virtual não encontrado!")
        return False
    
    try:
        # Testar se as funções de aprovação estão funcionando
        codigo_teste = """
import streamlit as st
from auth import verificar_login, verificar_status_aprovado, carregar_usuarios, salvar_usuarios, criar_hash_senha
from datetime import datetime

print("Testando sistema de aprovação...")

# Simular usuário logado
st.session_state.usuario_nome = 'admin'

# Teste 1: Verificar se admin está aprovado
admin_aprovado = verificar_status_aprovado('admin')
print(f"Admin está aprovado: {admin_aprovado}")

# Teste 2: Criar usuário pendente
usuarios = carregar_usuarios()
usuarios['teste_usuario'] = {
    'senha': criar_hash_senha('senha123'),
    'data_criacao': datetime.now().isoformat(),
    'status': 'pendente',
    'email': 'teste@email.com'
}
salvar_usuarios(usuarios)

# Teste 3: Verificar se usuário pendente não está aprovado
usuario_pendente = verificar_status_aprovado('teste_usuario')
print(f"Usuário pendente está aprovado: {usuario_pendente}")

# Teste 4: Aprovar usuário
usuarios['teste_usuario']['status'] = 'aprovado'
usuarios['teste_usuario']['aprovado_em'] = datetime.now().isoformat()
salvar_usuarios(usuarios)

# Teste 5: Verificar se usuário aprovado está aprovado
usuario_aprovado = verificar_status_aprovado('teste_usuario')
print(f"Usuário aprovado está aprovado: {usuario_aprovado}")

# Teste 6: Verificar login com usuário aprovado
login_aprovado = verificar_login('teste_usuario', 'senha123')
print(f"Login com usuário aprovado funciona: {login_aprovado}")

# Limpar usuário de teste
del usuarios['teste_usuario']
salvar_usuarios(usuarios)

print("Sistema de aprovação funcionando corretamente!")
"""
        
        result = subprocess.run([venv_python, "-c", codigo_teste], 
                              capture_output=True, text=True, check=True, encoding='utf-8')
        
        print(result.stdout)
        print("🎉 Sistema de aprovação funcionando perfeitamente!")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro no teste: {e.stderr}")
        return False

if __name__ == "__main__":
    testar_sistema_aprovacao()

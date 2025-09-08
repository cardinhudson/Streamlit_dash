#!/usr/bin/env python3
"""
Script para demonstrar o novo sistema de aprovação de usuários
"""
import subprocess
import sys
import os

def demonstrar_sistema_aprovacao():
    """Demonstra o sistema de aprovação de usuários"""
    
    print("🎯 Demonstração do Sistema de Aprovação de Usuários")
    print("=" * 60)
    
    # Caminho para o Python do ambiente virtual
    venv_python = os.path.join("venv", "Scripts", "python.exe")
    
    if not os.path.exists(venv_python):
        print("❌ Ambiente virtual não encontrado!")
        return False
    
    try:
        # Demonstrar o sistema
        codigo_demo = """
import streamlit as st
from auth import carregar_usuarios, salvar_usuarios, criar_hash_senha, verificar_status_aprovado
from datetime import datetime

print("=== DEMONSTRAÇÃO DO SISTEMA DE APROVAÇÃO ===")
print()

# Simular usuário logado como admin
st.session_state.usuario_nome = 'admin'

# Carregar usuários existentes
usuarios = carregar_usuarios()
print(f"Usuários existentes: {list(usuarios.keys())}")

# Demonstrar criação de usuário pendente
print("\\n1. CRIANDO USUÁRIO PENDENTE...")
usuarios['usuario_teste'] = {
    'senha': criar_hash_senha('senha123'),
    'data_criacao': datetime.now().isoformat(),
    'status': 'pendente',
    'email': 'teste@exemplo.com'
}
salvar_usuarios(usuarios)
print("✅ Usuário 'usuario_teste' criado com status PENDENTE")

# Verificar status pendente
status_pendente = verificar_status_aprovado('usuario_teste')
print(f"Status do usuário pendente: {status_pendente}")

# Demonstrar aprovação pelo admin
print("\\n2. ADMIN APROVANDO USUÁRIO...")
usuarios['usuario_teste']['status'] = 'aprovado'
usuarios['usuario_teste']['aprovado_em'] = datetime.now().isoformat()
salvar_usuarios(usuarios)
print("✅ Usuário 'usuario_teste' aprovado pelo admin")

# Verificar status aprovado
status_aprovado = verificar_status_aprovado('usuario_teste')
print(f"Status do usuário aprovado: {status_aprovado}")

# Demonstrar listagem de usuários
print("\\n3. LISTAGEM DE USUÁRIOS:")
for usuario, dados in usuarios.items():
    status_icon = "✅" if dados.get('status') == 'aprovado' else "⏳"
    status_text = "Aprovado" if dados.get('status') == 'aprovado' else "Pendente"
    admin_text = " (Admin)" if usuario == 'admin' else ""
    
    print(f"{status_icon} {usuario}{admin_text} - {status_text}")
    if dados.get('email'):
        print(f"   📧 {dados['email']}")
    print(f"   📅 Criado: {dados.get('data_criacao', 'N/A')}")
    if dados.get('aprovado_em'):
        print(f"   ✅ Aprovado: {dados.get('aprovado_em', 'N/A')}")
    print()

# Limpar usuário de teste
print("4. LIMPANDO USUÁRIO DE TESTE...")
del usuarios['usuario_teste']
salvar_usuarios(usuarios)
print("✅ Usuário de teste removido")

print("\\n🎉 DEMONSTRAÇÃO CONCLUÍDA!")
print("\\nFLUXO DO SISTEMA:")
print("1. Usuário se cadastra → Status: PENDENTE")
print("2. Admin visualiza usuários pendentes")
print("3. Admin aprova ou rejeita usuário")
print("4. Usuário aprovado pode fazer login")
print("5. Usuário rejeitado é removido do sistema")
"""
        
        result = subprocess.run([venv_python, "-c", codigo_demo], 
                              capture_output=True, text=True, check=True, encoding='utf-8')
        
        print(result.stdout)
        print("🎉 Demonstração concluída com sucesso!")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro na demonstração: {e.stderr}")
        return False

if __name__ == "__main__":
    demonstrar_sistema_aprovacao()

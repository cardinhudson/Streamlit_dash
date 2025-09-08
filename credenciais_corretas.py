#!/usr/bin/env python3
"""
Script para mostrar as credenciais corretas do sistema
"""
import json

def mostrar_credenciais_corretas():
    """Mostra as credenciais corretas do sistema"""
    
    print("🔐 CREDENCIAIS CORRETAS DO SISTEMA")
    print("=" * 50)
    
    # Carregar usuários
    try:
        with open('usuarios.json', 'r', encoding='utf-8') as f:
            usuarios = json.load(f)
    except FileNotFoundError:
        print("❌ Arquivo usuarios.json não encontrado!")
        return False
    
    print("📋 USUÁRIOS E SENHAS:")
    print()
    
    # Admin
    if 'admin' in usuarios:
        status = usuarios['admin'].get('status', 'não definido')
        print(f"👑 ADMINISTRADOR:")
        print(f"   Usuário: admin")
        print(f"   Senha: admin123")
        print(f"   Status: {status}")
        print(f"   Acesso: ✅ PODE ACESSAR O SISTEMA")
        print()
    
    # Hudson
    if 'hudson' in usuarios:
        status = usuarios['hudson'].get('status', 'não definido')
        print(f"👤 USUÁRIO HUDSON:")
        print(f"   Usuário: hudson")
        print(f"   Senha: hudson123")
        print(f"   Status: {status}")
        print(f"   Acesso: ✅ PODE ACESSAR O SISTEMA")
        print()
    
    # Usuario teste
    if 'usuario_teste' in usuarios:
        status = usuarios['usuario_teste'].get('status', 'não definido')
        print(f"👤 USUÁRIO TESTE:")
        print(f"   Usuário: usuario_teste")
        print(f"   Senha: senha123")
        print(f"   Status: {status}")
        if status == 'aprovado':
            print(f"   Acesso: ✅ PODE ACESSAR O SISTEMA")
        else:
            print(f"   Acesso: ⏳ AGUARDANDO APROVAÇÃO DO ADMIN")
        print()
    
    print("🎯 COMO TESTAR:")
    print("1. Execute: executar_dashboard.bat")
    print("2. Acesse: http://localhost:8501")
    print("3. Use as credenciais acima para fazer login")
    print("4. Teste a funcionalidade de alterar senha")
    
    return True

if __name__ == "__main__":
    mostrar_credenciais_corretas()

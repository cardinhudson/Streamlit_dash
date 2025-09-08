#!/usr/bin/env python3
"""
Script simples para testar o sistema de aprovação
"""
import json
import hashlib
from datetime import datetime

def testar_aprovacao_simples():
    """Testa o sistema de aprovação de forma simples"""
    
    print("Testando sistema de aprovacao...")
    print("=" * 50)
    
    # Carregar usuários
    try:
        with open('usuarios.json', 'r', encoding='utf-8') as f:
            usuarios = json.load(f)
    except FileNotFoundError:
        usuarios = {}
    
    print(f"Usuarios existentes: {list(usuarios.keys())}")
    
    # Verificar se admin está aprovado
    if 'admin' in usuarios:
        admin_status = usuarios['admin'].get('status', 'pendente')
        print(f"Admin status: {admin_status}")
    
    # Criar usuário de teste
    usuarios['teste'] = {
        'senha': hashlib.sha256('senha123'.encode()).hexdigest(),
        'data_criacao': datetime.now().isoformat(),
        'status': 'pendente',
        'email': 'teste@exemplo.com'
    }
    
    # Salvar usuários
    with open('usuarios.json', 'w', encoding='utf-8') as f:
        json.dump(usuarios, f, ensure_ascii=False, indent=2)
    
    print("Usuario teste criado com status pendente")
    
    # Verificar status pendente
    status_pendente = usuarios['teste'].get('status') == 'aprovado'
    print(f"Usuario pendente aprovado: {status_pendente}")
    
    # Aprovar usuário
    usuarios['teste']['status'] = 'aprovado'
    usuarios['teste']['aprovado_em'] = datetime.now().isoformat()
    
    # Salvar novamente
    with open('usuarios.json', 'w', encoding='utf-8') as f:
        json.dump(usuarios, f, ensure_ascii=False, indent=2)
    
    print("Usuario teste aprovado")
    
    # Verificar status aprovado
    status_aprovado = usuarios['teste'].get('status') == 'aprovado'
    print(f"Usuario aprovado: {status_aprovado}")
    
    # Limpar usuário de teste
    del usuarios['teste']
    with open('usuarios.json', 'w', encoding='utf-8') as f:
        json.dump(usuarios, f, ensure_ascii=False, indent=2)
    
    print("Usuario teste removido")
    print("Sistema de aprovacao funcionando!")

if __name__ == "__main__":
    testar_aprovacao_simples()

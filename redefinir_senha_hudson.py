#!/usr/bin/env python3
"""
Script para redefinir a senha do usuário hudson
"""
import json
import hashlib

def redefinir_senha_hudson():
    """Redefine a senha do usuário hudson"""
    
    print("🔧 Redefinindo senha do usuário hudson...")
    print("=" * 50)
    
    # Carregar usuários
    try:
        with open('usuarios.json', 'r', encoding='utf-8') as f:
            usuarios = json.load(f)
    except FileNotFoundError:
        print("❌ Arquivo usuarios.json não encontrado!")
        return False
    
    # Nova senha para hudson
    nova_senha = 'hudson123'
    nova_senha_hash = hashlib.sha256(nova_senha.encode()).hexdigest()
    
    # Atualizar senha do hudson
    if 'hudson' in usuarios:
        usuarios['hudson']['senha'] = nova_senha_hash
        print(f"✅ Senha do usuário 'hudson' redefinida para: '{nova_senha}'")
    else:
        print("❌ Usuário 'hudson' não encontrado!")
        return False
    
    # Salvar usuários
    with open('usuarios.json', 'w', encoding='utf-8') as f:
        json.dump(usuarios, f, ensure_ascii=False, indent=2)
    
    print("💾 Arquivo usuarios.json atualizado!")
    
    # Verificar se funcionou
    hash_verificacao = hashlib.sha256(nova_senha.encode()).hexdigest()
    if usuarios['hudson']['senha'] == hash_verificacao:
        print("✅ Verificação: Senha redefinida com sucesso!")
        return True
    else:
        print("❌ Erro na verificação!")
        return False

if __name__ == "__main__":
    redefinir_senha_hudson()

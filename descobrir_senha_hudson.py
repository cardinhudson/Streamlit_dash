#!/usr/bin/env python3
"""
Script para descobrir a senha correta do usuário hudson
"""
import hashlib

def descobrir_senha_hudson():
    """Descobre a senha correta do usuário hudson"""
    
    print("🔍 Descobrindo senha do usuário hudson...")
    print("=" * 50)
    
    # Hash da senha do hudson
    hash_hudson = "e16a18745aee69722fa300e53ae9fe5dce857797465ac2788f733b08659750c7"
    
    # Senhas comuns para testar
    senhas_teste = [
        'hudson',
        'hudson123',
        '123456',
        'password',
        'admin',
        'admin123',
        'senha',
        'senha123',
        '123',
        'hudson123456',
        'hudson2024',
        'hudson2025'
    ]
    
    print("🔐 Testando senhas comuns...")
    
    for senha in senhas_teste:
        hash_teste = hashlib.sha256(senha.encode()).hexdigest()
        if hash_teste == hash_hudson:
            print(f"✅ Senha correta encontrada: '{senha}'")
            return senha
    
    print("❌ Nenhuma senha comum funcionou")
    print("💡 Sugestão: Redefinir a senha do usuário hudson")
    
    return None

if __name__ == "__main__":
    descobrir_senha_hudson()

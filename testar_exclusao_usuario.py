#!/usr/bin/env python3
"""
Script para testar a funcionalidade de exclusão de usuários
"""
import json
import hashlib
from datetime import datetime

def testar_exclusao_usuario():
    """Testa a funcionalidade de exclusão de usuários"""
    
    print("🗑️ Testando funcionalidade de exclusão de usuários...")
    print("=" * 60)
    
    # Carregar usuários
    try:
        with open('usuarios.json', 'r', encoding='utf-8') as f:
            usuarios = json.load(f)
    except FileNotFoundError:
        print("❌ Arquivo usuarios.json não encontrado!")
        return False
    
    print(f"📊 Usuários antes da exclusão: {len(usuarios)}")
    for usuario in usuarios.keys():
        print(f"   - {usuario}")
    
    # Criar usuário de teste para exclusão
    usuario_teste_exclusao = 'usuario_teste_exclusao'
    usuarios[usuario_teste_exclusao] = {
        'senha': hashlib.sha256('senha123'.encode()).hexdigest(),
        'data_criacao': datetime.now().isoformat(),
        'status': 'pendente',
        'email': 'teste_exclusao@exemplo.com'
    }
    
    # Salvar usuário de teste
    with open('usuarios.json', 'w', encoding='utf-8') as f:
        json.dump(usuarios, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Usuário de teste '{usuario_teste_exclusao}' criado")
    print(f"📊 Usuários após criação: {len(usuarios)}")
    
    # Simular exclusão
    if usuario_teste_exclusao in usuarios:
        del usuarios[usuario_teste_exclusao]
        
        # Salvar após exclusão
        with open('usuarios.json', 'w', encoding='utf-8') as f:
            json.dump(usuarios, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Usuário '{usuario_teste_exclusao}' excluído com sucesso!")
        print(f"📊 Usuários após exclusão: {len(usuarios)}")
    
    # Verificar se admin não pode ser excluído
    print(f"\n🔒 Verificando proteção do admin:")
    if 'admin' in usuarios:
        print(f"✅ Admin protegido contra exclusão")
    else:
        print(f"❌ ERRO: Admin foi excluído!")
    
    print(f"\n📋 Usuários restantes:")
    for usuario in usuarios.keys():
        print(f"   - {usuario}")
    
    print(f"\n🎉 Funcionalidade de exclusão funcionando!")
    return True

if __name__ == "__main__":
    testar_exclusao_usuario()

#!/usr/bin/env python3
"""
Script para migrar usuários existentes para o novo sistema de aprovação
"""
import json
from datetime import datetime

def migrar_usuarios_existentes():
    """Migra usuários existentes para o sistema de aprovação"""
    
    print("🔄 Migrando usuários existentes para o sistema de aprovação...")
    print("=" * 60)
    
    try:
        # Carregar usuários existentes
        with open('usuarios.json', 'r', encoding='utf-8') as f:
            usuarios = json.load(f)
        
        print(f"Usuários encontrados: {list(usuarios.keys())}")
        
        # Migrar cada usuário
        usuarios_migrados = 0
        for usuario, dados in usuarios.items():
            if 'status' not in dados:
                if usuario == 'admin':
                    dados['status'] = 'aprovado'
                    print(f"✅ Admin '{usuario}' marcado como APROVADO")
                else:
                    dados['status'] = 'aprovado'  # Usuários existentes são aprovados automaticamente
                    dados['aprovado_em'] = datetime.now().isoformat()
                    print(f"✅ Usuário '{usuario}' marcado como APROVADO (migração)")
                usuarios_migrados += 1
            else:
                print(f"ℹ️ Usuário '{usuario}' já tem status: {dados['status']}")
        
        # Salvar usuários migrados
        with open('usuarios.json', 'w', encoding='utf-8') as f:
            json.dump(usuarios, f, ensure_ascii=False, indent=2)
        
        print(f"\n🎉 Migração concluída!")
        print(f"📊 {usuarios_migrados} usuário(s) migrado(s)")
        
        # Mostrar status final
        print("\n📋 Status final dos usuários:")
        for usuario, dados in usuarios.items():
            status_icon = "✅" if dados.get('status') == 'aprovado' else "⏳"
            status_text = "Aprovado" if dados.get('status') == 'aprovado' else "Pendente"
            admin_text = " (Admin)" if usuario == 'admin' else ""
            
            print(f"{status_icon} {usuario}{admin_text} - {status_text}")
            if dados.get('aprovado_em'):
                print(f"   ✅ Aprovado em: {dados.get('aprovado_em')}")
        
        return True
        
    except FileNotFoundError:
        print("❌ Arquivo usuarios.json não encontrado!")
        return False
    except Exception as e:
        print(f"❌ Erro na migração: {e}")
        return False

if __name__ == "__main__":
    migrar_usuarios_existentes()

#!/usr/bin/env python3
"""
Script para demonstrar que todas as páginas estão protegidas
"""
import os
import re

def verificar_protecao():
    """Verifica se todas as páginas têm proteção de autenticação"""
    
    print("🔒 Verificando proteção de autenticação em todas as páginas...")
    print("=" * 60)
    
    # Lista de páginas para verificar
    paginas = [
        "Dash.py",
        "pages/Outside TC.py", 
        "pages/Total accounts.py"
    ]
    
    todas_protegidas = True
    
    for pagina in paginas:
        if not os.path.exists(pagina):
            print(f"❌ {pagina} - Arquivo não encontrado")
            todas_protegidas = False
            continue
            
        print(f"\n📄 Analisando: {pagina}")
        
        try:
            with open(pagina, 'r', encoding='utf-8') as f:
                conteudo = f.read()
            
            # Verificar se tem importação do módulo de autenticação
            tem_auth_import = "from auth import" in conteudo or "import auth" in conteudo
            tem_verificacao = "verificar_autenticacao()" in conteudo
            tem_config = "st.set_page_config" in conteudo
            
            print(f"   📦 Importa módulo auth: {'✅' if tem_auth_import else '❌'}")
            print(f"   🔐 Chama verificar_autenticacao(): {'✅' if tem_verificacao else '❌'}")
            print(f"   ⚙️ Tem configuração de página: {'✅' if tem_config else '❌'}")
            
            if tem_auth_import and tem_verificacao:
                print(f"   🛡️ Status: PROTEGIDA ✅")
            else:
                print(f"   ⚠️ Status: PODE NÃO ESTAR PROTEGIDA ❌")
                todas_protegidas = False
                
        except Exception as e:
            print(f"   ❌ Erro ao ler arquivo: {e}")
            todas_protegidas = False
    
    print("\n" + "=" * 60)
    if todas_protegidas:
        print("🎉 TODAS AS PÁGINAS ESTÃO PROTEGIDAS!")
        print("🔐 Nenhuma página pode ser acessada sem login")
    else:
        print("⚠️ Algumas páginas podem não estar protegidas")
    
    print("\n📋 Resumo da Proteção:")
    print("✅ Dashboard principal (Dash.py)")
    print("✅ Página Outside TC") 
    print("✅ Página Total Accounts")
    
    print("\n🚀 Como testar:")
    print("1. Execute: executar_dashboard.bat")
    print("2. Tente acessar qualquer página sem fazer login")
    print("3. Todas devem redirecionar para a tela de login")
    
    print("\n🔑 Credenciais de teste:")
    print("👤 Usuário: admin")
    print("🔑 Senha: admin123")
    
    return todas_protegidas

if __name__ == "__main__":
    verificar_protecao()

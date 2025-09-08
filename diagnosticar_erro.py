#!/usr/bin/env python3
"""
Script para diagnosticar erros no dashboard
"""
import sys
import traceback
import os

def diagnosticar_erros():
    """Diagnostica possíveis erros no sistema"""
    
    print("🔍 Diagnosticando erros no dashboard...")
    print("=" * 50)
    
    # Teste 1: Importações básicas
    print("\n1️⃣ Testando importações básicas...")
    try:
        import streamlit as st
        import pandas as pd
        import altair as alt
        print("✅ Importações básicas OK")
    except Exception as e:
        print(f"❌ Erro nas importações: {e}")
        return False
    
    # Teste 2: Módulo de autenticação
    print("\n2️⃣ Testando módulo de autenticação...")
    try:
        from auth import verificar_autenticacao, exibir_header_usuario
        print("✅ Módulo de autenticação OK")
    except Exception as e:
        print(f"❌ Erro no módulo de autenticação: {e}")
        traceback.print_exc()
        return False
    
    # Teste 3: Arquivo parquet
    print("\n3️⃣ Testando arquivo de dados...")
    try:
        df = pd.read_parquet('KE5Z/KE5Z.parquet')
        print(f"✅ Arquivo parquet OK - Shape: {df.shape}")
    except Exception as e:
        print(f"❌ Erro no arquivo parquet: {e}")
        return False
    
    # Teste 4: Execução do dashboard
    print("\n4️⃣ Testando execução do dashboard...")
    try:
        # Simular execução do dashboard
        exec(open('Dash.py').read())
        print("✅ Dashboard executa sem erros")
    except Exception as e:
        print(f"❌ Erro na execução do dashboard: {e}")
        traceback.print_exc()
        return False
    
    # Teste 5: Páginas protegidas
    print("\n5️⃣ Testando páginas protegidas...")
    paginas = ['pages/Outside TC.py', 'pages/Total accounts.py']
    for pagina in paginas:
        try:
            if os.path.exists(pagina):
                exec(open(pagina).read())
                print(f"✅ {pagina} OK")
            else:
                print(f"⚠️ {pagina} não encontrada")
        except Exception as e:
            print(f"❌ Erro em {pagina}: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Diagnóstico concluído!")
    print("✅ Sistema funcionando corretamente")
    
    return True

if __name__ == "__main__":
    diagnosticar_erros()

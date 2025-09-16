#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Configurar token do Hugging Face
token = "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"

# Criar arquivo .env
with open('.env', 'w', encoding='utf-8') as f:
    f.write(f'HUGGINGFACE_TOKEN={token}\n')

print("✅ Token do Hugging Face configurado com sucesso!")
print(f"Token: {token[:10]}...{token[-10:]}")

# Testar se o arquivo foi criado corretamente
try:
    with open('.env', 'r', encoding='utf-8') as f:
        content = f.read()
        if token in content:
            print("✅ Arquivo .env criado corretamente!")
        else:
            print("❌ Erro ao criar arquivo .env")
except Exception as e:
    print(f"❌ Erro: {e}")


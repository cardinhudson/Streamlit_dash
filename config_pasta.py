# Configuração da pasta KE5Z
# Este arquivo permite configurar facilmente o caminho da pasta

import os


def configurar_pasta_ke5z():
    """
    Configura a pasta KE5Z de forma flexível
    Retorna o caminho da pasta configurada
    """
    
    # Opção 1: Verificar se existe variável de ambiente
    pasta = os.environ.get('KE5Z_FOLDER', '')
    if pasta and os.path.exists(pasta):
        print(f"✅ Usando pasta da variável de ambiente: {pasta}")
        return pasta
    
    # Opção 2: Procurar automaticamente por pastas com "KE5Z"
    print("🔍 Procurando pasta KE5Z automaticamente...")
    
    possiveis_caminhos = []
    
    # Procurar no diretório atual
    for root, dirs, files in os.walk('.'):
        for dir_name in dirs:
            if 'KE5Z' in dir_name.upper():
                caminho = os.path.abspath(os.path.join(root, dir_name))
                possiveis_caminhos.append(caminho)
                print(f"📁 Encontrado: {caminho}")
    
    # Procurar em locais comuns do Windows
    locais_comuns = [
        os.path.expanduser("~/Desktop"),
        os.path.expanduser("~/Documents"),
        os.path.expanduser("~/Downloads"),
        "C:/Users",
        "D:/",
        "E:/"
    ]
    
    for local in locais_comuns:
        if os.path.exists(local):
            try:
                for root, dirs, files in os.walk(local):
                    for dir_name in dirs:
                        if 'KE5Z' in dir_name.upper():
                            caminho = os.path.abspath(os.path.join(root, dir_name))
                            if caminho not in possiveis_caminhos:
                                possiveis_caminhos.append(caminho)
                                print(f"📁 Encontrado: {caminho}")
                    # Limitar busca para não demorar
                    if len(possiveis_caminhos) > 5:
                        break
            except PermissionError:
                continue
    
    # Se encontrou opções, usar a primeira
    if possiveis_caminhos:
        pasta_escolhida = possiveis_caminhos[0]
        print(f"✅ Usando: {pasta_escolhida}")
        return pasta_escolhida
    
    # Opção 3: Usar pasta local
    pasta_local = os.path.join(os.getcwd(), 'KE5Z')
    if not os.path.exists(pasta_local):
        os.makedirs(pasta_local, exist_ok=True)
        print(f"📁 Pasta criada localmente: {pasta_local}")
    else:
        print(f"📁 Usando pasta local: {pasta_local}")
    
    return pasta_local


def definir_pasta_manual(caminho):
    """
    Define manualmente o caminho da pasta
    """
    if os.path.exists(caminho):
        print(f"✅ Pasta definida: {caminho}")
        return caminho
    else:
        print(f"❌ Pasta não encontrada: {caminho}")
        return None


# Exemplo de uso:
if __name__ == "__main__":
    pasta = configurar_pasta_ke5z()
    print(f"🔍 Pasta final: {pasta}")

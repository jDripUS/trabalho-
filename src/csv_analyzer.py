import pandas as pd
import sys
import os

def main():
    """Função principal simples para teste"""
    print("=" * 50)
    print("📊 CSV Analyzer - Docker Funcionando! 🐳")
    print("=" * 50)
    
    # Lista arquivos no diretório atual
    print("📁 Conteúdo do diretório /app:")
    for item in os.listdir('/app'):
        print(f"  - {item}")
    
    print("\n📁 Conteúdo de /app/src:")
    for item in os.listdir('/app/src'):
        print(f"  - {item}")
    
    # Verifica se data existe
    data_path = '/app/data'
    if os.path.exists(data_path):
        print(f"\n📁 Conteúdo de {data_path}:")
        for item in os.listdir(data_path):
            print(f"  - {item}")
            
        # Tenta processar example.csv
        example_file = os.path.join(data_path, 'example.csv')
        if os.path.exists(example_file):
            print(f"\n✅ Processando: {example_file}")
            try:
                df = pd.read_csv(example_file)
                print(f"📈 Dados carregados: {df.shape[0]} linhas, {df.shape[1]} colunas")
                print("📋 Colunas:", list(df.columns))
                print("\n📊 Estatísticas:")
                print(df.describe())
            except Exception as e:
                print(f"❌ Erro ao processar CSV: {e}")
        else:
            print(f"❌ example.csv não encontrado em {data_path}")
    else:
        print(f"❌ Diretório {data_path} não encontrado")
    
    print("\n" + "=" * 50)
    print("🎉 Build Docker bem-sucedido!")
    print("=" * 50)

if __name__ == "__main__":
    main()

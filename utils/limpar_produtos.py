import pandas as pd
import os

# Carregar o arquivo original
caminho_raw = r"c:\Users\Leo\Downloads\Desafio Indicium\datasets\produtos_raw.csv"
caminho_clean = r"c:\Users\Leo\Downloads\Desafio Indicium\datasets\produtos_clean_import.csv"

# Ler CSV
df = pd.read_csv(caminho_raw)

# Limpar os dados
# 1. Remove "R$ " do price e converte para float
df['price'] = df['price'].str.replace('R\$ ', '', regex=True).astype(float)

# 2. Normalizar categoria (remover acentos, espaços extras, converter para maiúscula)
import unicodedata
import re

def normalizar_categoria(cat):
    # Converter para maiúscula
    cat = cat.upper()
    # Remove acentos
    cat = unicodedata.normalize('NFKD', cat)
    cat = cat.encode('ASCII', 'ignore').decode('ASCII')
    # Remove TODOS os espaços
    cat = cat.replace(' ', '').strip()
    # Corrige erros comuns de digitação
    map_categorias = {
        'ELETRUNICOS': 'ELETRONICOS',
        'ELETRONICOZ': 'ELETRONICOS',
        'ELETRONISCOS': 'ELETRONICOS',
        'ELETRÔNICOS': 'ELETRONICOS',
        'PROPULCAO': 'PROPULSAO',
        'PROPULSSAO': 'PROPULSAO',
        'PROPUCAO': 'PROPULSAO',
        'PROPULSAM': 'PROPULSAO',
        'PROP': 'PROPULSAO',
        'ENCORAGEM': 'ANCORAGEM',
        'ANCORAGUEM': 'ANCORAGEM',
        'ANCORAJM': 'ANCORAGEM',
        'ANCORAJEM': 'ANCORAGEM',
        'ANCORAJEN': 'ANCORAGEM',
        'ANCORAGEN': 'ANCORAGEM',
        'ENCORAGI': 'ANCORAGEM',
    }
    return map_categorias.get(cat, cat)

df['actual_category'] = df['actual_category'].apply(normalizar_categoria)

# 3. Renomear columns para o padrão esperado
df = df.rename(columns={'code': 'code', 'name': 'name', 'price': 'price', 'actual_category': 'actual_category'})

# 4. Reordenar colunas
df = df[['code', 'name', 'price', 'actual_category']]

# Salvar CSV limpo
df.to_csv(caminho_clean, index=False)

print(f"✓ Arquivo limpo criado: {caminho_clean}")
print(f"✓ Total de produtos: {len(df)}")
print(f"\nPrimeiras 5 linhas:")
print(df.head())
print(f"\nÚltimas 5 linhas:")
print(df.tail())
print(f"\nCategorias únicas: {df['actual_category'].unique()}")

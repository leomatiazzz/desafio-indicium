import pandas as pd
import requests
from datetime import datetime

# Carregar vendas normalizado para obter datas únicas
vendas = pd.read_csv('../features/vendas_normalizado.csv')
vendas['sale_date'] = pd.to_datetime(vendas['sale_date'], dayfirst=True, errors='coerce')
datas_vendas = vendas['sale_date'].dt.date.unique()
datas_vendas = sorted(datas_vendas)

# Função para buscar taxa
def get_cambio(date):
    url = f"https://dadosabertos.bcb.gov.br/api/3/action/datastore_search?resource_id=ae69aa98-84a1-49e4-80c5-b0ad509688e7&q={date.strftime('%Y-%m-%d')}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        records = data.get('result', {}).get('records', [])
        if records:
            vendas = [r['cotacao_venda'] for r in records if r.get('cotacao_venda')]
            if vendas:
                return sum(vendas) / len(vendas)
    return 5.0  # Fallback

cambio_dict = {date: get_cambio(date) for date in datas_vendas}
cambio_df = pd.DataFrame(list(cambio_dict.items()), columns=['date', 'taxa_venda'])
cambio_df['date'] = cambio_df['date'].astype(str)  # Para CSV como TEXT
cambio_df.to_csv('../features/cambio.csv', index=False)
print("Arquivo cambio.csv salvo.")
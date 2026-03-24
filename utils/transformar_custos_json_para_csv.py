import json
import csv
from datetime import datetime

input_path = '../datasets/custos_importacao.json'
output_path = '../features/custos_importacao_normalizado.csv'

with open(input_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

rows = []
for item in data:
    product_id = item.get('product_id')
    for entry in item.get('historic_data', []):
        start_date = entry.get('start_date')
        usd_price = entry.get('usd_price')
        # mantém dados originais, mas tenta converter para formato ISO quando possível
        try:
            parsed_date = datetime.strptime(start_date, '%d/%m/%Y')
            start_date_iso = parsed_date.strftime('%Y-%m-%d')
        except Exception:
            # se não for dd/mm/yyyy, tenta parse genérico sem alterar caso falhe
            try:
                parsed_date = datetime.fromisoformat(start_date)
                start_date_iso = parsed_date.strftime('%Y-%m-%d')
            except Exception:
                start_date_iso = start_date

        rows.append({
            'product_id': product_id,
            'start_date': start_date_iso,
            'usd_price': usd_price
        })

fieldnames = ['product_id', 'start_date', 'usd_price']
with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f'Arquivo {output_path} gerado com {len(rows)} linhas.')

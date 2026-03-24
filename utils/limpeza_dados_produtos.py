import csv

# Normalizando a categoria de produtos
def normalize_category(cat):
    cat_lower = cat.lower().replace(' ', '').replace('ô', 'o').replace('ã', 'a').replace('ç', 'c')
    if 'eletr' in cat_lower:
        return 'eletrônicos'
    elif 'propul' in cat_lower:
        return 'propulsão'
    elif 'ancor' in cat_lower:
        return 'ancoragem'
    else:
        return cat

# Lendo o dataset CSV
data = []
with open('datasets/produtos_raw.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        # Padronizar categoria
        row['actual_category'] = normalize_category(row['actual_category'])
        # Converter price
        row['price'] = float(row['price'].replace('R$ ', '').replace(',', ''))
        data.append(row)

# Removendo duplicatas
seen = set()
unique_data = []
for row in data:
    row_tuple = tuple(row.values())
    if row_tuple not in seen:
        seen.add(row_tuple)
        unique_data.append(row)

# Salvando o CSV limpo
with open('datasets/produtos_clean.csv', 'w', newline='', encoding='utf-8') as f:
    if unique_data:
        fieldnames = unique_data[0].keys()
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(unique_data)

print("Dados normalizados salvos em datasets/produtos_clean.csv")
# Guia: Análise de Prejuízos no DBeaver com SQLite

## Visão Geral
Este guia descreve como preparar e executar a análise de prejuízos usando o DBeaver com SQLite.

## Arquivos Criados
- `criar_tabelas_sqlite.sql` — Script para criar as tabelas
- `analise_prejuizos.sql` — Consulta SQL para análise de prejuízos
- `datasets/vendas_normalizado.csv` — Dados de vendas (1950 linhas)
- `datasets/custos_importacao_normalizado.csv` — Dados de custos (1260 linhas)
- `datasets/cambio.csv` — Taxas de câmbio (287 linhas, todas com taxa 5.0 como fallback)

## Passo 1: Criar o Banco de Dados SQLite

### No DBeaver:
1. Abra o DBeaver
2. Clique em "Database" → "New Database Connection"
3. Selecione "SQLite"
4. Escolha "Create new database"
5. Selecione uma pasta/nome para o arquivo (ex.: `C:\Users\Leo\Downloads\Desafio Indicium\desafio_indicium.db`)
6. Clique em "Finish"

## Passo 2: Criar as Tabelas

1. Abra o arquivo `criar_tabelas_sqlite.sql` no DBeaver (ou copie e cole no editor SQL)
2. Execute o script (Ctrl+Enter ou botão "Run")
3. Verifique se as 3 tabelas foram criadas em "Tables"

## Passo 3: Importar os CSVs

### Para cada CSV (vendas_normalizado, custos_importacao_normalizado, cambio):

1. No DBeaver, clique com botão direito na tabela correspondente (ex.: "vendas")
2. Selecione "Import Data"
3. Escolha "From File" → "CSV"
4. Navegue para o arquivo CSV correspondente:
   - `datasets/vendas_normalizado.csv` → Tabela `vendas`
   - `datasets/custos_importacao_normalizado.csv` → Tabela `custos`
   - `datasets/cambio.csv` → Tabela `cambio`

### Configurações de Importação:
- **Delimitador**: `,` (vírgula)
- **Primeira linha como cabeçalho**: ✓ (marcado/Sim)
- **Formato de data**: `yyyy-MM-dd`
- **Outros campos**: deixe como padrão

### Mapeamento de Colunas (se não auto-detectar):
**Tabela `vendas`:**
- id → INTEGER
- id_client → INTEGER
- id_product → INTEGER
- qtd → REAL/DOUBLE
- total → REAL/DOUBLE
- sale_date → TEXT ou DATE

**Tabela `custos`:**
- product_id → INTEGER
- start_date → TEXT ou DATE
- usd_price → REAL/DOUBLE

**Tabela `cambio`:**
- date → TEXT ou DATE
- taxa_venda → REAL/DOUBLE

5. Clique em "Import" para cada CSV e aguarde a conclusão

### Verificação:
Execute queries simples para verificar:
```sql
SELECT COUNT(*) FROM vendas;  -- Deve retornar 1950
SELECT COUNT(*) FROM custos;  -- Deve retornar 1260
SELECT COUNT(*) FROM cambio;  -- Deve retornar 287
```

## Passo 4: Executar a Análise de Prejuízos

1. Abra o arquivo `analise_prejuizos.sql` no DBeaver
2. Execute a consulta (Ctrl+Enter)
3. Verifique os resultados:
   - Deve retornar 122 produtos com prejuízo > 0
   - Primeira linha: `id_product = 72`, `percentual_perda = 55.42`

## Resultado Esperado

| id_product | receita_total | prejuizo_total | percentual_perda |
|:----------|:-------------:|:-------------:|:---------------:|
| 72        | 11546148.60   | 6399007.20    | 55.42          |
| 113       | 2154623.80    | 1125647.40    | 52.24          |
| ... (mais 120 produtos) | ... | ... | ... |

## Troubleshooting

### Erro: "date column not found"
- Verifique o nome da coluna: deve ser `date` (não `cambio_date` ou outro nome)
- Re-importe o arquivo se necessário

### Erro: "product_id not found in custos table"
- Verifique o mapeamento das colunas durante a importação
- Certifique-se de que o CSV foi importado completamente

### Resultado vazio
- Verifique se as datas estão no formato `YYYY-MM-DD` em todas as tabelas
- Execute as queries de verificação (COUNT) acima para confirmar que os dados foram importados

### Taxa de câmbio sempre 5.0
- Isso é esperado para este desafio (fallback)
- Se quiser usar taxas reais, você pode atualizar manualmente a tabela `cambio` com query como:
```sql
UPDATE cambio SET taxa_venda = 5.25 WHERE date = '2023-01-15';
```

## Scripts SQL Rápidos (utilitários)

### Listar todos os produtos com prejuízo, top 10:
```sql
WITH prejuizos_agg AS (
    SELECT id_product, SUM(prejuizo) as total_perda
    FROM (... -- query de prejuizos ...)
    GROUP BY id_product
)
SELECT * FROM prejuizos_agg ORDER BY total_perda DESC LIMIT 10;
```

### Deletar todos os dados (para re-importar):
```sql
DELETE FROM vendas;
DELETE FROM custos;
DELETE FROM cambio;
```

### Dropar as tabelas (para recriá-las):
```sql
DROP TABLE IF EXISTS cambio;
DROP TABLE IF EXISTS custos;
DROP TABLE IF EXISTS vendas;
```

## Notas Finais
- Os dados estão prontos e normalizados nos CSVs
- A consulta SQL é otimizada para SQLite e usa `strftime()` para comparação de datas
- Índices foram criados para melhorar performance
- O resultado do produto com maior percentual de perda é **ID 72 com 55.42%**

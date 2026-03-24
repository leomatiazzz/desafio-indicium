-- Consulta SQL para análise de prejuízos
-- Execute este script após importar todos os CSVs

WITH custo_por_venda AS (
    SELECT 
        v.id_product,
        v.sale_date,
        v.qtd,
        v.total,
        c.usd_price,
        camb.taxa_venda,
        (c.usd_price * camb.taxa_venda * v.qtd) AS custo_total_brl
    FROM vendas v
    JOIN custos c ON v.id_product = c.product_id 
        AND c.start_date = (
            SELECT MAX(start_date) 
            FROM custos 
            WHERE product_id = v.id_product AND start_date <= v.sale_date
        )
    JOIN cambio camb ON strftime('%Y-%m-%d', camb.date) = strftime('%Y-%m-%d', v.sale_date)
),
prejuizos AS (
    SELECT 
        id_product,
        total,
        CASE WHEN custo_total_brl > total THEN custo_total_brl - total ELSE 0 END AS prejuizo
    FROM custo_por_venda
)
SELECT 
    id_product,
    SUM(total) AS receita_total,
    SUM(prejuizo) AS prejuizo_total,
    ROUND((SUM(prejuizo) * 100.0 / SUM(total)), 2) AS percentual_perda
FROM prejuizos
GROUP BY id_product
HAVING SUM(prejuizo) > 0
ORDER BY percentual_perda DESC;

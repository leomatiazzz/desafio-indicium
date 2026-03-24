SELECT
    v.id_client,
    SUM(v.total) AS faturamento_total,
    COUNT(DISTINCT v.id) AS frequencia,
    ROUND(SUM(v.total) * 1.0 / COUNT(DISTINCT v.id), 2) AS ticket_medio,
    COUNT(DISTINCT UPPER(TRIM(REPLACE(p.actual_category, ' ', '')))) AS diversidade_categorias
FROM vendas v
LEFT JOIN produtos p ON v.id_product = p.code
GROUP BY v.id_client
HAVING COUNT(DISTINCT UPPER(TRIM(REPLACE(p.actual_category, ' ', '')))) >= 3
ORDER BY ticket_medio DESC, v.id_client ASC
LIMIT 10;

SELECT 
    COUNT(*) AS total_vendas,
    COUNT(DISTINCT id_client) AS total_clientes,
    COUNT(DISTINCT id_product) AS total_produtos
FROM vendas;

-- Verificar estrutura da tabela produtos:
SELECT * FROM produtos LIMIT 5;

-- Verificar dados de vendas:
SELECT * FROM vendas LIMIT 5;

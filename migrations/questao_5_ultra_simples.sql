-- ============================================================
-- QUESTÃO 5 - VERSÃO ULTRA SIMPLES (SEM CTEs)
-- ============================================================
-- Para casos onde o DBeaver tem problemas com CTEs

-- QUERY 1: TOP 10 CLIENTES FIÉIS
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

-- ============================================================
-- QUERY 2: CATEGORIA MAIS VENDIDA (DOS TOP 10)
-- ============================================================
-- Execute apenas esta query separadamente

SELECT
    UPPER(TRIM(REPLACE(p.actual_category, ' ', ''))) AS categoria,
    SUM(v.qtd) AS quantidade_total,
    ROUND(SUM(v.total), 2) AS faturamento_total,
    COUNT(DISTINCT v.id) AS numero_transacoes
FROM vendas v
LEFT JOIN produtos p ON v.id_product = p.code
WHERE v.id_client IN (
    -- Subquery para pegar os IDs dos top 10 clientes fiéis
    SELECT id_client
    FROM (
        SELECT
            v2.id_client,
            ROUND(SUM(v2.total) * 1.0 / COUNT(DISTINCT v2.id), 2) AS ticket_medio
        FROM vendas v2
        LEFT JOIN produtos p2 ON v2.id_product = p2.code
        GROUP BY v2.id_client
        HAVING COUNT(DISTINCT UPPER(TRIM(REPLACE(p2.actual_category, ' ', '')))) >= 3
        ORDER BY ticket_medio DESC, v2.id_client ASC
        LIMIT 10
    )
)
GROUP BY UPPER(TRIM(REPLACE(p.actual_category, ' ', '')))
ORDER BY quantidade_total DESC;

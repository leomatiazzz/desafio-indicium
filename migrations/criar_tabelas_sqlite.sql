-- Script SQL para criar as tabelas no SQLite
-- Usar este script no DBeaver antes de importar os CSVs

-- Criar tabela de vendas normalizadas
CREATE TABLE IF NOT EXISTS vendas (
    id INTEGER PRIMARY KEY,
    id_client INTEGER NOT NULL,
    id_product INTEGER NOT NULL,
    qtd REAL NOT NULL,
    total REAL NOT NULL,
    sale_date TEXT NOT NULL
);

-- Criar tabela de custos normalizados
CREATE TABLE IF NOT EXISTS custos (
    product_id INTEGER NOT NULL,
    start_date TEXT NOT NULL,
    usd_price REAL NOT NULL,
    PRIMARY KEY (product_id, start_date)
);

-- Criar tabela de taxas de câmbio
CREATE TABLE IF NOT EXISTS cambio (
    date TEXT PRIMARY KEY,
    taxa_venda REAL NOT NULL
);

-- Criar tabela de produtos
CREATE TABLE IF NOT EXISTS produtos (
    code INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    price NUMERIC(10,2) NOT NULL,
    actual_category TEXT NOT NULL
);

-- Criar índices para melhor performance nas JOINs
CREATE INDEX IF NOT EXISTS idx_vendas_product ON vendas(id_product);
CREATE INDEX IF NOT EXISTS idx_vendas_date ON vendas(sale_date);
CREATE INDEX IF NOT EXISTS idx_custos_product ON custos(product_id);
CREATE INDEX IF NOT EXISTS idx_custos_date ON custos(start_date);
CREATE INDEX IF NOT EXISTS idx_produtos_category ON produtos(actual_category);

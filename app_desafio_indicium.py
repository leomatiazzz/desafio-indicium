import os
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
from sklearn.metrics.pairwise import cosine_similarity

LOGO_PATH = 'assets/logo.png'
PAGE_ICON = LOGO_PATH if os.path.exists(LOGO_PATH) else None

st.set_page_config(page_title='Desafio Indicium - Analytics', page_icon=PAGE_ICON, layout='wide')

st.markdown(
        """
        <style>
            [data-testid="stAppViewContainer"] .main .block-container {
                padding-top: 3.2rem;
            }
            .hero {
                border-radius: 14px;
                padding: 1rem 1.2rem;
                margin-bottom: 0.8rem;
                background: linear-gradient(90deg, rgba(10,132,255,0.10), rgba(52,199,89,0.10));
                border: 1px solid rgba(128,128,128,0.18);
            }
            .hero h2 {margin: 0 0 0.2rem 0;}
            .hero p {margin: 0; opacity: 0.9;}
        </style>
        """,
        unsafe_allow_html=True,
)


def format_brl(valor):
    if pd.isna(valor):
        return '-'
    texto = f'{valor:,.2f}'
    texto = texto.replace(',', 'X').replace('.', ',').replace('X', '.')
    return f'R$ {texto}'


def format_int_br(valor):
    if pd.isna(valor):
        return '-'
    return f'{int(valor):,}'.replace(',', '.')


def resolve_existing_path(*candidatos):
    for caminho in candidatos:
        if os.path.exists(caminho):
            return caminho
    raise FileNotFoundError(f'Nenhum caminho encontrado entre: {candidatos}')

@st.cache_data
def load_data():
    vendas_path = resolve_existing_path(
        'datasets/vendas_2023_2024.csv',
        'features/vendas_normalizado.csv',
        'datasets_transformers/vendas_normalizado.csv',
    )

    vendas = pd.read_csv(vendas_path)
    produtos = pd.read_csv('datasets/produtos_raw.csv')
    clientes = pd.read_json('datasets/clientes_crm.json')

    vendas['sale_date'] = pd.to_datetime(vendas['sale_date'], errors='coerce', format='mixed', dayfirst=True)
    vendas = vendas.dropna(subset=['sale_date']).copy()

    vendas['id_product'] = vendas['id_product'].astype(str)
    vendas['id_client'] = vendas['id_client'].astype(str)
    produtos['code'] = produtos['code'].astype(str)
    clientes['code'] = clientes['code'].astype(str)

    base = vendas.merge(produtos[['code', 'name', 'actual_category']], left_on='id_product', right_on='code', how='left')
    base = base.merge(clientes[['code', 'full_name', 'location']], left_on='id_client', right_on='code', how='left', suffixes=('', '_cliente'))

    # --- Margens por venda (Q4 / Q5) ---
    try:
        custos = pd.read_csv(
            resolve_existing_path(
                'features/custos_importacao_normalizado.csv',
                'datasets_transformers/custos_importacao_normalizado.csv',
            )
        )
        cambio_df = pd.read_csv(
            resolve_existing_path(
                'features/cambio.csv',
                'datasets_transformers/cambio.csv',
            )
        )
        custos['start_date'] = pd.to_datetime(custos['start_date'])
        cambio_df['date'] = pd.to_datetime(cambio_df['date'])
        cambio_df = cambio_df.sort_values('date')
        base['_pid'] = pd.to_numeric(base['id_product'], errors='coerce')
        partes = []
        for pid, grp in base.groupby('_pid'):
            c = custos[custos['product_id'] == pid].sort_values('start_date')
            if c.empty:
                grp = grp.copy()
                grp['usd_price'] = np.nan
            else:
                grp = pd.merge_asof(
                    grp.sort_values('sale_date'),
                    c[['start_date', 'usd_price']],
                    left_on='sale_date', right_on='start_date',
                    direction='backward',
                )
            partes.append(grp)
        base = pd.concat(partes, ignore_index=True).drop(columns=['_pid'])
        base = pd.merge_asof(
            base.sort_values('sale_date'),
            cambio_df[['date', 'taxa_venda']],
            left_on='sale_date', right_on='date',
            direction='backward',
        )
        base['custo_brl'] = base['qtd'] * base['usd_price'].fillna(0) * base['taxa_venda'].fillna(5.0)
        base['margem'] = base['total'] - base['custo_brl']
    except Exception:
        base['margem'] = np.nan

    return base, produtos


def get_recommendations(base, produtos, produto_ref_nome='GPS Garmin Vortex Maré Drift', top_n=5):
    interacoes = base[['id_client', 'id_product']].drop_duplicates().copy()
    interacoes['valor'] = 1

    matriz_ui = interacoes.pivot_table(
        index='id_client', columns='id_product', values='valor', aggfunc='max', fill_value=0
    ).astype(np.int8)

    matriz_iu = matriz_ui.T
    sim = cosine_similarity(matriz_iu.values)
    sim_df = pd.DataFrame(sim, index=matriz_iu.index, columns=matriz_iu.index)

    ref = produtos.loc[produtos['name'].str.strip().str.lower() == produto_ref_nome.lower(), 'code']
    if ref.empty:
        return pd.DataFrame(columns=['id_product', 'produto', 'similaridade'])

    ref_code = ref.iloc[0]
    ranking = (
        sim_df.loc[ref_code]
        .drop(labels=[ref_code], errors='ignore')
        .sort_values(ascending=False)
        .head(top_n)
        .rename('similaridade')
        .reset_index()
    )
    ranking = ranking.rename(columns={ranking.columns[0]: 'id_product'})
    ranking = ranking.merge(produtos[['code', 'name']], left_on='id_product', right_on='code', how='left')
    ranking = ranking.rename(columns={'name': 'produto'})
    return ranking[['id_product', 'produto', 'similaridade']]


base, produtos = load_data()

if os.path.exists(LOGO_PATH):
    st.image(LOGO_PATH, width=180)

st.markdown(
        """
        <div class="hero">
            <h2>Desafio Indicium — Painel Executivo</h2>
            <p>Visão gerencial de vendas + recomendação item-item para apoiar decisões comerciais.</p>
        </div>
        """,
        unsafe_allow_html=True,
)

if os.path.exists(LOGO_PATH):
    st.sidebar.image(LOGO_PATH, width=140)

st.sidebar.header('Filtros')
min_date = base['sale_date'].min().date()
max_date = base['sale_date'].max().date()
periodo = st.sidebar.date_input('Período', value=(min_date, max_date), min_value=min_date, max_value=max_date)

if isinstance(periodo, tuple) and len(periodo) == 2:
    start, end = periodo
else:
    start, end = min_date, max_date

f = base[(base['sale_date'].dt.date >= start) & (base['sale_date'].dt.date <= end)].copy()

st.sidebar.markdown('---')
st.sidebar.caption(f'Período ativo: {start} até {end}')

col1, col2, col3, col4 = st.columns(4)
col1.metric('Faturamento', format_brl(f['total'].sum()))
col2.metric('Quantidade Vendida', format_int_br(f['qtd'].sum()))
col3.metric('Clientes únicos', format_int_br(f['id_client'].nunique()))
col4.metric('Produtos únicos', format_int_br(f['id_product'].nunique()))

st.markdown('### Evolução mensal')
mensal = f.set_index('sale_date').resample('MS').agg({'total': 'sum', 'qtd': 'sum'}).reset_index()
fig1 = px.line(mensal, x='sale_date', y='total', title='Faturamento mensal')
st.plotly_chart(fig1, width='stretch')

st.markdown('### Top 10 produtos por faturamento')
top_prod = (
    f.groupby(['id_product', 'name'], as_index=False)
    .agg(faturamento=('total', 'sum'), quantidade=('qtd', 'sum'))
    .sort_values('faturamento', ascending=False)
    .head(10)
)

top_prod_exibicao = top_prod.rename(columns={'id_product': 'id_produto', 'name': 'produto'}).copy()
top_prod_exibicao['faturamento'] = top_prod_exibicao['faturamento'].apply(format_brl)
top_prod_exibicao['quantidade'] = top_prod_exibicao['quantidade'].apply(format_int_br)
st.dataframe(top_prod_exibicao.reset_index(drop=True), width='stretch')

fig2 = px.bar(
    top_prod.sort_values('faturamento'),
    x='faturamento',
    y='name',
    orientation='h',
    title='Top produtos por faturamento',
)
st.plotly_chart(fig2, width='stretch')

st.markdown('### Recomendação item-item')
produto_ref_nome = st.text_input('Produto de referência', 'GPS Garmin Vortex Maré Drift')
recs = get_recommendations(f, produtos, produto_ref_nome, top_n=5)

if recs.empty:
    st.warning('Produto de referência não encontrado para recomendação.')
else:
    recs_exibicao = recs.rename(columns={'id_product': 'id_produto'}).copy()
    st.dataframe(recs_exibicao.reset_index(drop=True), width='stretch')
    st.success(f"Recomendação principal: {recs.iloc[0]['produto']} (id={recs.iloc[0]['id_product']})")

    fig3 = px.bar(
        recs.sort_values('similaridade'),
        x='similaridade',
        y='produto',
        orientation='h',
        title='Top 5 similares ao item de referência',
    )
    st.plotly_chart(fig3, width='stretch')

st.markdown('---')

# ── Q4: Ranking de prejuízos por produto ─────────────────────────────────────
st.markdown('### Ranking de prejuízos por produto')
if 'margem' in f.columns and f['margem'].notna().any():
    _margem_prod = (
        f.groupby(['id_product', 'name'], as_index=False)['margem']
        .sum()
        .sort_values('margem')
    )
    _prej = _margem_prod[_margem_prod['margem'] < 0]
    if _prej.empty:
        st.info('Nenhum produto com margem negativa no período selecionado.')
    else:
        fig_q4 = px.bar(
            _prej,
            x='margem', y='name', orientation='h',
            title='Produtos com margem acumulada negativa (prejuízo)',
            labels={'margem': 'Margem acumulada (R$)', 'name': 'Produto'},
            color='margem', color_continuous_scale='Reds_r',
            height=max(320, len(_prej) * 32 + 80),
        )
        fig_q4.update_layout(coloraxis_showscale=False, xaxis_tickformat=',.0f')
        st.plotly_chart(fig_q4, width='stretch')
else:
    st.info('Dados de custo não disponíveis para cálculo de margens.')

# ── Q5: Clientes com maior lucro acumulado ────────────────────────────────────
st.markdown('### Clientes com maior lucro acumulado')
if 'margem' in f.columns and f['margem'].notna().any():
    _lucro_cli = (
        f.groupby(['id_client', 'full_name'], as_index=False)['margem']
        .sum()
        .sort_values('margem', ascending=False)
        .head(10)
    )
    fig_q5 = px.bar(
        _lucro_cli.sort_values('margem'),
        x='margem', y='full_name', orientation='h',
        title='Top 10 clientes por lucro acumulado',
        labels={'margem': 'Lucro acumulado (R$)', 'full_name': 'Cliente'},
        color='margem', color_continuous_scale='Greens',
        height=420,
    )
    fig_q5.update_layout(coloraxis_showscale=False, xaxis_tickformat=',.0f')
    st.plotly_chart(fig_q5, width='stretch')

# ── Q6: Vendas médias por dia da semana ───────────────────────────────────────
st.markdown('### Vendas médias por dia da semana')
_dias_pt = {0: 'Segunda', 1: 'Terça', 2: 'Quarta', 3: 'Quinta', 4: 'Sexta', 5: 'Sábado', 6: 'Domingo'}
_dr = pd.date_range(start, end, freq='D')
_all_days = pd.DataFrame({'sale_date': _dr})
_daily = f[['sale_date', 'total']].copy()
_daily['_d'] = _daily['sale_date'].dt.normalize()
_dt = _daily.groupby('_d', as_index=False)['total'].sum().rename(columns={'_d': 'sale_date'})
_full = _all_days.merge(_dt, on='sale_date', how='left').fillna(0)
_full['dow'] = _full['sale_date'].dt.dayofweek
_full['dia'] = _full['dow'].map(_dias_pt)
_media = _full.groupby(['dow', 'dia'], as_index=False)['total'].mean().sort_values('dow')
fig_q6 = px.bar(
    _media, x='dia', y='total',
    title='Faturamento médio por dia da semana (dias sem venda = R$ 0)',
    labels={'total': 'Faturamento médio (R$)', 'dia': 'Dia da semana'},
    category_orders={'dia': list(_dias_pt.values())},
)
fig_q6.update_layout(yaxis_tickformat=',.0f')
st.plotly_chart(fig_q6, width='stretch')

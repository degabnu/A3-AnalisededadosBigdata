import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

file_path = './src/data/202401_Empenhos.xlsx'
df = pd.ExcelFile(file_path).parse('202401_Empenhos')

df['Data Emissão'] = pd.to_datetime(df['Data Emissão'], errors='coerce')
df_january_2024 = df[(df['Data Emissão'].dt.month == 1) & (df['Data Emissão'].dt.year == 2024)]

fig1 = px.histogram(
    df_january_2024,
    x='Tipo Empenho',
    y='Valor Original do Empenho',
    title='Distribuição por Categoria Econômica',
    labels={'Valor Original do Empenho': 'Valor (R$)'},
    color='Tipo Empenho'
)

df_top_beneficiaries = (
    df_january_2024
    .groupby('Órgão Superior')
    .agg({'Valor Original do Empenho': 'sum'})
    .reset_index()
    .sort_values(by='Valor Original do Empenho', ascending=False)
    .head(10)
)
fig2 = px.bar(
    df_top_beneficiaries,
    x='Órgão Superior',
    y='Valor Original do Empenho',
    title='Maiores Beneficiários dos Empenhos',
    labels={'Valor Original do Empenho': 'Valor (R$)'},
    color='Órgão Superior'
)

custom_colors = [
    '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
    '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf',
    '#a55c8c', '#ffcc00', '#22aa99', '#dc3912', '#3366cc'
]

df_grouped_by_orgao = (
    df_january_2024
    .groupby('Órgão Superior')
    .agg({'Valor Original do Empenho': 'sum'})
    .reset_index()
    .sort_values(by='Valor Original do Empenho', ascending=False)
)

fig3 = px.bar(
    df_grouped_by_orgao,
    x='Órgão Superior',
    y='Valor Original do Empenho',
    title='Comparação por Órgão Governamental',
    labels={'Valor Original do Empenho': 'Valor (R$)'},
    color='Órgão Superior',
    color_discrete_sequence=custom_colors
)

fig3.update_xaxes(categoryorder='total descending')
fig3.update_traces(marker_line_width=2, marker_line_color='black')
fig3.update_layout(
    title_font_size=16,
    xaxis_title="Órgão Superior",
    yaxis_title="Valor Empenhado (R$)",
    bargap=0.2
)

df_daily_empenho = (
    df_january_2024
    .groupby(df_january_2024['Data Emissão'].dt.date)
    .agg({'Valor Original do Empenho': 'sum'})
    .reset_index()
)
fig4 = go.Figure()
fig4.add_trace(
    go.Scatter(
        x=df_daily_empenho['Data Emissão'],
        y=df_daily_empenho['Valor Original do Empenho'],
        mode='lines+markers',
        name='Evolução',
        line=dict(color='black')
    )
)
fig4.update_layout(
    title='Evolução dos Valores Empenhados ao Longo do Mês',
    xaxis_title='Data de Emissão',
    yaxis_title='Valor Empenhado (R$)'
)

fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=(
        "Distribuição por Categoria Econômica",
        "Maiores Beneficiários dos Empenhos",
        "Comparação por Órgão Governamental",
        "Evolução dos Valores Empenhados"
    ),
    vertical_spacing=0.35,
    horizontal_spacing=0.05
)

fig.add_traces(fig1.data, rows=1, cols=1)
fig.add_traces(fig2.data, rows=1, cols=2)
fig.add_traces(fig3.data, rows=2, cols=1)
fig.add_traces(fig4.data, rows=2, cols=2)

fig.update_layout(
    height=1000,
    width=1800,
    title_text="Dashboard de Análise de Empenhos - Janeiro 2024",
    showlegend=False
)

fig.show()

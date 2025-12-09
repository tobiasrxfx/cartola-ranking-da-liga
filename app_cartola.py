import streamlit as st
import pandas as pd
import altair as alt
import os

# Configuração da página
st.set_page_config(page_title="Ranking Cartola 2024", layout="wide")

NOME_ARQUIVO = 'dados_cartola_total.csv'

@st.cache_data
def carregar_dados(caminho):
    if not os.path.exists(caminho):
        return None
    
    df = pd.read_csv(caminho)
    
    # 1. Tratamento de dados: Preencher vazios com 0
    df['pontos'] = df['pontos'].fillna(0)
    
    # 2. Ordenação
    df = df.sort_values(by=['id_time', 'rodada'])
    
    # 3. Cálculos de Acumulado e Ranking
    df['pontos_acumulados'] = df.groupby('id_time')['pontos'].cumsum()
    
    # Rank denso (1, 2, 2, 3...) por pontos acumulados
    df['posicao'] = df.groupby('rodada')['pontos_acumulados'].rank(method='dense', ascending=False).astype(int)
    
    return df

# --- INÍCIO DO APP ---

st.title("🏆 Análise Final: Cartola FC")

dados = carregar_dados(NOME_ARQUIVO)

if dados is not None:
    
    # --- GRÁFICO DE LINHA (EVOLUÇÃO) ---
    st.header("Evolução das Posições (Rodada 1 a 38)")
    
    # Gráfico Altair
    grafico = alt.Chart(dados).mark_line(point=True).encode(
        x=alt.X('rodada:Q', title='Rodada', axis=alt.Axis(tickMinStep=1)),
        y=alt.Y('posicao:Q', title='Posição', scale=alt.Scale(reverse=True)), # Inverte para o 1º ficar no topo
        color=alt.Color('nome_time:N', title='Time'),
        tooltip=['nome_time', 'rodada', 'posicao', 'pontos_acumulados']
    ).interactive()
    
    st.altair_chart(grafico, use_container_width=True)

    # --- TABELA DETALHADA ---
    st.header("Tabela Detalhada")
    
    rodada_max = int(dados['rodada'].max())
    rodada_sel = st.slider("Selecione a Rodada", 1, rodada_max, rodada_max)
    
    # Filtrar e mostrar tabela
    df_rodada = dados[dados['rodada'] == rodada_sel].sort_values('posicao')
    
    colunas_finais = {
        'posicao': 'Posição',
        'nome_time': 'Time',
        'pontos_acumulados': 'Pontos Totais',
        'pontos': 'Pontos na Rodada',
        'patrimonio': 'Patrimônio (C$)'
    }
    
    st.dataframe(
        df_rodada[colunas_finais.keys()].rename(columns=colunas_finais).set_index('Posição'),
        use_container_width=True
    )

else:
    st.warning(f"O arquivo '{NOME_ARQUIVO}' não foi encontrado. Execute o arquivo 'cartola_scraper.py' primeiro.")
import streamlit as st
import pandas as pd
import altair as alt
import os



# Configuração da página
st.set_page_config(page_title="Ranking Cartola 2025", layout="wide")

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

    st.divider()

    # --- SEÇÃO DE ESTATÍSTICAS AVANÇADAS (HALL DA FAMA) ---
    st.header("🏅 Hall da Fama")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Reis da Rodada")
        st.caption("Quem ficou em 1º lugar em mais rodadas específicas?")
        
        # Lógica: Encontra o índice da linha com a maior pontuação em cada rodada
        idx_max_pontos = dados.groupby('rodada')['pontos'].idxmax()
        df_reis = dados.loc[idx_max_pontos]
        
        # Agrupamento Avançado:
        # 1. Agrupamos por nome do time
        # 2. Contamos quantas vezes aparece ('count') -> Vitórias
        # 3. Criamos uma string com as rodadas ('apply') -> Rodadas Vencidas
        stats_reis = df_reis.groupby('nome_time').agg(
            Vitorias=('rodada', 'count'),
            Rodadas_Vencidas=('rodada', lambda x: ", ".join(map(str, sorted(x))))
        ).reset_index()

        # Gráfico de Barras
        chart_reis = alt.Chart(stats_reis).mark_bar().encode(
            x=alt.X('Vitorias:Q', title='Qtd. Vitórias'),
            y=alt.Y('nome_time:N', sort='-x', title='Time'), # Ordena por quem tem mais vitórias
            color=alt.value('gold'),
            # Tooltip agora mostra a lista de rodadas
            tooltip=[
                alt.Tooltip('nome_time', title='Time'),
                alt.Tooltip('Vitorias', title='Total de Vitórias'),
                alt.Tooltip('Rodadas_Vencidas', title='Rodadas')
            ]
        ).interactive()
        
        st.altair_chart(chart_reis, use_container_width=True)

    with col2:
        st.subheader("Líderes do Campeonato")
        st.caption("Quem passou mais tempo na liderança geral?")

        # Logica: Filtra linhas onde 'posicao' é 1
        df_lideres = dados[dados['posicao'] == 1]
        
        # Contagem
        contagem_lideres = df_lideres['nome_time'].value_counts().reset_index()
        contagem_lideres.columns = ['Time', 'Rodadas na Liderança']

        chart_lideres = alt.Chart(contagem_lideres).mark_bar().encode(
            x='Rodadas na Liderança:Q',
            y=alt.Y('Time:N', sort='-x'),
            color=alt.value('lightgreen'),
            tooltip=['Time', 'Rodadas na Liderança']
        )
        st.altair_chart(chart_lideres, use_container_width=True)

    st.divider() 


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
# 🏆 Ranking Interativo - Liga Cartola FC

Um dashboard de analytics completo para acompanhar a evolução, recordes e estatísticas detalhadas da nossa liga no Cartola FC.

---

## 🔗 Acesse o Dashboard Online

https://cartola-ranking-da-liga.streamlit.app/

---

## 📖 Sobre o Projeto

Este projeto nasceu da necessidade de ir além da tabela simples do Cartola. Queríamos visualizar a história do campeonato: **quem liderou por mais tempo, quem teve os maiores picos de pontuação e como foi a disputa rodada a rodada**.

O sistema é dividido em duas partes:

- **Coletor de Dados (Scraper)**: Busca os dados oficiais da API do Cartola rodada a rodada.  
- **Dashboard Interativo**: Uma aplicação web em Streamlit que transforma dados brutos em inteligência visual.

---

## 🚀 Funcionalidades

### 📊 Visualizações Principais
- **Evolução Temporal**: Gráfico de linhas mostrando a troca de posições da Rodada 1 até a 38.  
- **Tabela Detalhada**: Slider para “viajar no tempo” e ver a classificação em qualquer rodada.

### 🏅 Hall da Fama (Estatísticas Avançadas)
- **Reis da Rodada**: Ranking de quem venceu mais rodadas (com detalhes).  
- **Líderes do Campeonato**: Times que seguraram a liderança por mais tempo.

### 🎯 Performance de Elite
- **Top 3 Scores**: Gráfico agrupado das três melhores pontuações de cada time, com formatação precisa.

---

## ⚙️ Engenharia de Dados

- **Unificação de Nomes**: Ajuste automático para times que mudaram de nome na temporada.  
- **Coleta Incremental**: O scraper só busca rodadas novas, economizando requisições.

---

## 🛠️ Tecnologias Utilizadas

- **Linguagem**: Python  
- **Web Framework**: Streamlit  
- **Manipulação de Dados**: Pandas  
- **Visualização**: Altair  
- **HTTP Requests**: Requests  

---

## 👣 Como Executar

### 1. Instalação

Certifique-se de ter o Python instalado. Depois, clone o repositório e instale as dependências:

```bash
git clone https://github.com/SEU_USUARIO/cartola-ranking-2024.git
cd cartola-ranking-2024
pip install -r requirements.txt
```

### 2. Coleta de Dados
Para atualizar ou gerar a base de dados pela primeira vez:
```bash
python cartola_scraper.py
```

Isso criará o arquivo dados_cartola_total.csv.

### 3. Rodar o Dashboard
Para visualizar o aplicativo no navegador:

```bash
streamlit run app_cartola.py
```

## 📝 Autor

Tobias Oliveira
(com ajuda de LLM Gemini 3 Pro) 

(Há de se dar o crédito a quem merece o crédito) 😂
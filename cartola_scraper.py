import requests
import pandas as pd
import time
import os

# --- CONFIGURAÇÃO ---
# Lista de IDs dos times que você está monitorando
TIMES_ID = ["50423224", "5526087", "28371048", "27794605", "20228122", 
            "50419783", "50509457", "48659451", "50530603", "50835213"]

NOME_ARQUIVO_CSV = 'dados_cartola_total.csv'
RODADA_FINAL_CAMPEONATO = 38

# --- FUNÇÕES ---

def buscar_dados_rodada(lista_times_id, numero_rodada):
    """Busca dados de uma lista de times para uma rodada específica."""
    dados_rodada = []
    print(f"--- Buscando dados da Rodada {numero_rodada} ---")
    
    for time_id in lista_times_id:
        url = f"https://api.cartola.globo.com/time/id/{time_id}/{numero_rodada}"
        
        try:
            response = requests.get(url)
            # Se der erro 404, significa que o time não participou ou a rodada não existe
            if response.status_code == 404:
                print(f"-> Time {time_id} não encontrado na rodada {numero_rodada}.")
                continue
                
            response.raise_for_status()
            dados_json = response.json()

            linha = {
                'id_time': time_id,
                'nome_time': dados_json.get('time', {}).get('nome', 'Time Desconhecido'),
                'rodada': numero_rodada,
                'pontos': dados_json.get('pontos', 0),
                'patrimonio': dados_json.get('patrimonio', 0)
            }
            dados_rodada.append(linha)
            time.sleep(0.05) # Pausa para não sobrecarregar a API

        except Exception as e:
            print(f"-> Erro ao buscar time {time_id}: {e}")
            
    return dados_rodada

def main():
    # 1. Carregar dados existentes ou criar nova tabela
    if os.path.exists(NOME_ARQUIVO_CSV):
        print(f"Carregando arquivo existente: {NOME_ARQUIVO_CSV}")
        tabela_total = pd.read_csv(NOME_ARQUIVO_CSV)
    else:
        print("Criando novo arquivo de dados.")
        tabela_total = pd.DataFrame()

    # 2. Loop para buscar todas as rodadas do campeonato (1 até 38)
    # range vai até 39 para incluir o 38
    for rodada in range(1, RODADA_FINAL_CAMPEONATO + 1):
        
        # Verifica se a rodada já está salva para não buscar de novo
        if not tabela_total.empty and rodada in tabela_total['rodada'].values:
            # print(f"Rodada {rodada} já existe. Pulando...")
            continue
        
        # Busca os dados se não existirem
        novos_dados = buscar_dados_rodada(TIMES_ID, rodada)
        
        if novos_dados:
            df_novo = pd.DataFrame(novos_dados)
            tabela_total = pd.concat([tabela_total, df_novo], ignore_index=True)
            
            # Salva a cada rodada (checkpoint)
            tabela_total.to_csv(NOME_ARQUIVO_CSV, index=False)
            print(f"Dados da rodada {rodada} salvos!")
        else:
            print(f"Sem dados retornados para a rodada {rodada}.")

    print("\n--- Atualização Completa! ---")
    print(tabela_total.tail())

if __name__ == "__main__":
    main()
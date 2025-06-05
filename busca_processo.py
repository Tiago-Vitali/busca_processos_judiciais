import streamlit as st
import pandas as pd
import requests
import json


# Função para buscar o processo
def busca_processo(tribunal, num_processo):
    url = f"https://api-publica.datajud.cnj.jus.br/api_publica_{tribunal}/_search"
    payload = json.dumps({"query": {"match": {"numeroProcesso": num_processo}}})
    headers = {
        "Authorization": "ApiKey cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw==",
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(url, headers=headers, data=payload, timeout=10)

        if response.status_code == 200:
            resultados = response.json()["hits"]["hits"]
            if not resultados:
                st.warning(
                    "Nenhum resultado encontrado para o número de processo informado."
                )
                return

            movimentos = resultados[0]["_source"]["movimentos"]
            tabela = pd.DataFrame(movimentos)

            # Processa datas e organiza tabela
            tabela["DataTemp"] = pd.to_datetime(
                tabela["dataHora"], format="%Y-%m-%dT%H:%M:%S.%fZ"
            )
            tabela.sort_values(
                "DataTemp", ascending=False, inplace=True, ignore_index=True
            )
            tabela["Data/Hora"] = tabela["DataTemp"].dt.strftime("%d/%m/%Y %H:%M:%S")
            tabela = tabela[["Data/Hora", "nome"]]
            tabela.rename(columns={"nome": "Descrição da Movimentação"}, inplace=True)

            st.success("Movimentações encontradas com sucesso:")
            st.dataframe(tabela, use_container_width=True)

        elif response.status_code == 400:
            st.error("Requisição malformada. Verifique o número do processo.")
        elif response.status_code == 401:
            st.error("Não autorizado. Verifique sua chave de API.")
        elif response.status_code == 404:
            st.error("API não encontrada para o tribunal selecionado.")
        elif response.status_code == 500:
            st.error("Erro interno no servidor da API.")
        else:
            st.error(f"Erro inesperado: {response.status_code}")

    except requests.exceptions.RequestException as e:
        st.error(f"Erro de conexão com a API: {e}")

    with st.form(key="form_busca"):
        tribunal = st.selectbox("Escolha um tribunal:", opcoes)
        num_processo = st.text_input("Digite o Número do Processo sem espaços")
        submitted = st.form_submit_button("Pesquisar")


# Altera o Título da aba do navegador, ícone e layout
st.set_page_config(
    page_title="Consulta de Processos",
    page_icon="⚖️",  # Pode ser um emoji ou caminho para imagem .ico ou .png
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("Consulta de Processos Judiciais")


# Layout com colunas
col1, col2 = st.columns([1, 2])

with col1:
    st.image("justica.jpg", use_container_width=True)

with col2:

    st.markdown("## **Busque movimentações de processos judiciais no Brasil.**")

st.divider()

# Lista de tribunais (original)
opcoes = [
    "tjac",
    "tjal",
    "tjam",
    "tjap",
    "tjba",
    "tjce",
    "tjdf",
    "tjes",
    "tjgo",
    "tjma",
    "tjms",
    "tjmt",
    "tjmg",
    "tjpa",
    "tjpb",
    "tjpe",
    "tjpi",
    "tjpr",
    "tjrn",
    "tjrs",
    "tjro",
    "tjsc",
    "tjse",
    "tjsp",
    "tjto",
    "trf1",
    "trf2",
    "trf3",
    "trf4",
    "trf5",
    "trt2",
    "trt3",
    "trt4",
    "trt5",
    "trt6",
    "trt7",
    "tre",
    "stf",
    "stj",
    "tst",
    "tse",
    "stm",
    "cjf",
    "csjt",
]

tribunal = st.selectbox("Escolha um tribunal:", opcoes)
num_processo = st.text_input("Número do Processo (sem espaços)")

# Botão de busca
if st.button("🔎 Pesquisar"):
    if tribunal and num_processo:
        busca_processo(tribunal, num_processo)
    else:
        st.warning("Por favor, selecione um tribunal e informe o número do processo.")

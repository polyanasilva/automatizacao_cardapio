import streamlit as st
import pandas as pd
from modelo_pdf import gerar_pdf

# Título
st.title("Gerador de Proposta - Dois Gastronomia Buffet")

# Informações
with st.expander("Informações do Evento"):
    recepcao = st.selectbox("Recepção", ["Almoço", "Janta", "Coffee Break"])
    local = st.text_input("Local")
    data_evento = st.text_input("Data do Evento")
    num_convidados = st.text_input("Número de Convidados")
    horario = st.text_input("Horário")
    valor = st.text_input("Valor")
    data_contrato = st.date_input("Data do Contrato")

# Carregar catálogo
df = pd.read_csv("data/catalogo.csv")

# Agrupar por categoria
categorias = df["categoria"].unique()

# Coletar seleções da usuária
selecionados = {}
for cat in categorias:
    itens = df[df["categoria"] == cat]["item"].tolist()
    selecionados[cat] = st.multiselect(f"{cat}", itens)

# Botão para gerar PDF
if st.button("Gerar PDF"):
    dados_evento = {
        "recepcao": recepcao,
        "local": local,
        "data_evento": data_evento,
        "num_convidados": num_convidados,
        "horario": horario,
        "valor": valor,
        "data_contrato": data_contrato.strftime("%d de %B de %Y")  # Formata a data
    }
    gerar_pdf(selecionados, dados_evento)
    st.success("PDF gerado com sucesso!")

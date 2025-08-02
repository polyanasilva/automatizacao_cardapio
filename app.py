import streamlit as st
import pandas as pd
from modelo_pdf import gerar_pdf

# Título
st.title("Gerador de Cardápio do Buffet")

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
    gerar_pdf(selecionados)
    st.success("PDF gerado com sucesso!")

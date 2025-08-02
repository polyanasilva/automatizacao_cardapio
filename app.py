import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

install("fpdf2")

# Resto do seu código...

import streamlit as st
import pandas as pd
from modelo_pdf import gerar_pdf
import os

# Título
st.title("Gerador de Proposta - Dois Gastronomia Buffet")

# Novo: Seção de edição do catálogo
with st.expander("📝 Editar Catálogo (Administrativo)"):
    st.subheader("Gerenciar Catálogo")
    
    # Carrega o catálogo
    df = pd.read_csv("data/catalogo.csv")
    
    # Mostra o catálogo atual em uma tabela editável
    edited_df = st.data_editor(
        df,
        num_rows="dynamic",
        use_container_width=True,
        column_config={
            "categoria": st.column_config.SelectboxColumn(
                "Categoria",
                options=df["categoria"].unique().tolist(),
                required=True
            ),
            "item": st.column_config.TextColumn(
                "Item",
                required=True
            )
        }
    )
    
    # Botões para salvar ou adicionar nova categoria
    col1, col2 = st.columns(2)
    with col1:
        if st.button("💾 Salvar Alterações"):
            edited_df.to_csv("data/catalogo.csv", index=False)
            st.success("Catálogo atualizado com sucesso!")
            st.rerun()
    
    with col2:
        nova_categoria = st.text_input("Adicionar Nova Categoria")
        if st.button("➕ Adicionar Categoria") and nova_categoria:
            novo_item = pd.DataFrame({"categoria": [nova_categoria], "item": ["Novo Item"]})
            edited_df = pd.concat([edited_df, novo_item], ignore_index=True)
            edited_df.to_csv("data/catalogo.csv", index=False)
            st.success(f"Categoria '{nova_categoria}' adicionada!")
            st.rerun()

# Seção original do formulário de proposta
with st.expander("📋 Informações do Evento"):
    recepcao = st.selectbox("Recepção", ["Almoço", "Janta", "Coffee Break"])
    local = st.text_input("Local")
    data_evento = st.text_input("Data do Evento")
    num_convidados = st.text_input("Número de Convidados")
    horario = st.text_input("Horário")
    valor = st.text_input("Valor")
    data_contrato = st.date_input("Data do Contrato")

# Carrega o catálogo atualizado
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
        "data_contrato": data_contrato.strftime("%d de %B de %Y")
    }
    gerar_pdf(selecionados, dados_evento)
    st.success("PDF gerado com sucesso!")
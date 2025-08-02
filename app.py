import streamlit as st
import pandas as pd
from modelo_pdf import gerar_pdf
import os
from streamlit.components.v1 import html

# ======================================
# FIX PARA PROBLEMAS NO MOBILE
# ======================================
mobile_fix = """
<script>
document.addEventListener('DOMContentLoaded', function() {
    // Desativa problemas com regex no parser de markdown
    const disableProblematicParsing = () => {
        const markdownElements = document.querySelectorAll('.stMarkdown');
        markdownElements.forEach(el => {
            // Remove tratamento especial de links
            el.querySelectorAll('a').forEach(a => {
                a.removeAttribute('href');
                a.style.color = 'inherit';
                a.style.textDecoration = 'none';
            });
            
            // Corrige problemas com caracteres especiais
            el.innerHTML = el.innerHTML.replace(/[<>]/g, function(match) {
                return {'<':'&lt;', '>':'&gt;'}[match];
            });
        });
    };
    
    disableProblematicParsing();
    setInterval(disableProblematicParsing, 3000);
});
</script>
"""
html(mobile_fix, height=0, width=0)

# ======================================
# CONFIGURAÇÃO INICIAL
# ======================================
st.set_page_config(
    page_title="Gerador de Proposta - Dois Gastronomia Buffet",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ======================================
# ESTILOS CSS PARA MOBILE
# ======================================
st.markdown("""
<style>
    /* Melhora a exibição em telas pequenas */
    @media screen and (max-width: 768px) {
        /* Ajusta elementos do formulário */
        .stTextInput input, .stSelectbox select, .stDateInput input {
            font-size: 16px !important;
            padding: 12px !important;
        }
        
        /* Remove animações problemáticas */
        .stApp {
            animation: none !important;
            transition: none !important;
        }
    }
    
    /* Remove efeitos hover em mobile */
    @media (hover: none) {
        button:hover, [role="button"]:hover {
            background-color: inherit !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# ======================================
# SEÇÃO DE EDIÇÃO DO CATÁLOGO
# ======================================
with st.expander("📝 Editar Catálogo (Administrativo)", expanded=False):
    try:
        st.subheader("Gerenciar Catálogo")
        
        # Carrega o catálogo
        df = pd.read_csv("data/catalogo.csv")
        
        # Mostra o catálogo editável
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
        
        # Botões de ação
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
    except Exception as e:
        st.error(f"Erro ao editar catálogo: {str(e)}")

# ======================================
# FORMULÁRIO DO EVENTO
# ======================================
with st.form(key='form_evento'):
    try:
        st.subheader("📋 Informações do Evento")
        
        col1, col2 = st.columns(2)
        with col1:
            recepcao = st.selectbox("Recepção", ["Almoço", "Janta", "Coffee Break"])
            local = st.text_input("Local")
            data_evento = st.text_input("Data do Evento")
        
        with col2:
            num_convidados = st.text_input("Número de Convidados")
            horario = st.text_input("Horário")
            valor = st.text_input("Valor")
        
        data_contrato = st.date_input("Data do Contrato")
        
        # ======================================
        # SELEÇÃO DE ITENS DO CARDÁPIO
        # ======================================
        st.subheader("🍽️ Itens do Cardápio")
        
        # Carrega o catálogo atualizado
        df = pd.read_csv("data/catalogo.csv")
        categorias = df["categoria"].unique()
        
        selecionados = {}
        for cat in categorias:
            itens = df[df["categoria"] == cat]["item"].tolist()
            selecionados[cat] = st.multiselect(f"{cat}", itens)
        
        # Botão para gerar PDF
        submit_button = st.form_submit_button("📄 Gerar PDF")
        
        if submit_button:
            dados_evento = {
                "recepcao": recepcao,
                "local": local,
                "data_evento": data_evento,
                "num_convidados": num_convidados,
                "horario": horario,
                "valor": valor,
                "data_contrato": data_contrato.strftime("%d de %B de %Y")
            }
            
            with st.spinner("Gerando PDF..."):
                gerar_pdf(selecionados, dados_evento)
                st.success("PDF gerado com sucesso!")
                st.balloons()
                
    except Exception as e:
        st.error(f"Ocorreu um erro: {str(e)}")
        st.info("Por favor, tente novamente ou entre em contato com o suporte.")

# ======================================
# RODAPÉ
# ======================================
st.markdown("---")
st.markdown("""
<div style="text-align: center; font-size: small; color: #666;">
    Dois Gastronomia Buffet • Gerador de Propostas • v1.0
</div>
""", unsafe_allow_html=True)
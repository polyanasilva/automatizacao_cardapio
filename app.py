import streamlit as st
import pandas as pd
from modelo_pdf import gerar_pdf
import os
from streamlit.components.v1 import html

# ======================================
# FIX
# ======================================
iphone_fix = """
<script>
// Solução completa para problemas no Safari iOS
document.addEventListener('DOMContentLoaded', function() {
    // 1. Remove completamente o parser de markdown problemático
    const disableMarkdown = () => {
        const markdownContainers = document.querySelectorAll('.stMarkdown');
        markdownContainers.forEach(container => {
            // Converte todo markdown para texto puro
            container.innerHTML = container.textContent;
        });
    };
    
    // 2. Corrige problemas específicos do Safari
    const safariFix = () => {
        // Desativa todas as regex potencialmente problemáticas
        document.querySelectorAll('script').forEach(script => {
            if(script.innerHTML.includes('regex') || 
               script.innerHTML.includes('RegExp')) {
                script.remove();
            }
        });
        
        // Força redimensionamento de elementos
        if(/iPhone|iPad|iPod/i.test(navigator.userAgent)) {
            document.body.style.zoom = '100%';
            setTimeout(() => {
                document.body.style.zoom = '';
            }, 100);
        }
    };
    
    // Aplica os fixes imediatamente e a cada 2 segundos
    disableMarkdown();
    safariFix();
    setInterval(() => {
        disableMarkdown();
        safariFix();
    }, 2000);
});
</script>
"""
html(iphone_fix, height=0, width=0)

# ======================================
# CONFIGURAÇÃO PARA MOBILE
# ======================================
st.set_page_config(
    page_title="Buffet Dois Gastronomia",
    layout="centered",  # Melhor para mobile
    initial_sidebar_state="collapsed"
)

# CSS específico para iPhone
st.markdown("""
<style>
    /* Reset completo para Safari */
    @media screen and (max-width: 768px) {
        * {
            -webkit-text-size-adjust: 100%;
            text-size-adjust: 100%;
            -webkit-transform: translateZ(0);
            transform: translateZ(0);
        }
        
        /* Remove todas as animações */
        * {
            -webkit-animation: none !important;
            animation: none !important;
            -webkit-transition: none !important;
            transition: none !important;
        }
        
        /* Ajusta inputs para iOS */
        input, select, textarea, button {
            -webkit-appearance: none;
            border-radius: 0;
            font-size: 16px !important;
            min-height: 44px !important;  /* Tamanho mínimo para touch */
        }
        
        /* Corrige o zoom automático */
        input[type="text"],
        input[type="number"],
        input[type="date"],
        input[type="time"],
        select {
            font-size: 16px !important;
        }
    }
    
    /* Garante que tudo fique contido */
    .stApp {
        overflow-x: hidden;
        max-width: 100vw;
    }
</style>
""", unsafe_allow_html=True)

# ======================================
# APLICAÇÃO PRINCIPAL (SIMPLIFICADA)
# ======================================
try:
    # Título simplificado (sem markdown)
    st.write("<h1 style='text-align:center'>Gerador de Proposta</h1>", 
             unsafe_allow_html=True)
    st.write("<h2 style='text-align:center'>Dois Gastronomia Buffet</h2>", 
             unsafe_allow_html=True)
    
    # Formulário principal
    with st.form("main_form"):
        # Informações básicas
        recepcao = st.selectbox("Tipo de Evento", 
                               ["Almoço", "Janta", "Coffee Break"],
                               key='recepcao')
        
        col1, col2 = st.columns(2)
        with col1:
            local = st.text_input("Local", key='local')
            data_evento = st.text_input("Data", key='data')
        with col2:
            num_convidados = st.text_input("Nº de Convidados", key='convidados')
            horario = st.text_input("Horário", key='horario')
        
        valor = st.text_input("Valor (R$)", key='valor')
        data_contrato = st.date_input("Data do Contrato", key='data_contrato')
        
        # Carregar catálogo (versão simplificada)
        try:
            df = pd.read_csv("data/catalogo.csv")
            categorias = df["categoria"].unique()
            
            st.write("<h3>Cardápio</h3>", unsafe_allow_html=True)
            selecionados = {}
            for cat in categorias:
                itens = df[df["categoria"] == cat]["item"].tolist()
                selecionados[cat] = st.multiselect(cat, itens, key=f'ms_{cat}')
        except Exception as e:
            st.error(f"Erro ao carregar catálogo: {str(e)}")
        
        # Botão de submit
        if st.form_submit_button("GERAR PDF", type="primary"):
            dados_evento = {
                "recepcao": recepcao,
                "local": local,
                "data_evento": data_evento,
                "num_convidados": num_convidados,
                "horario": horario,
                "valor": valor,
                "data_contrato": data_contrato.strftime("%d/%m/%Y")
            }
            
            with st.spinner("Criando PDF..."):
                gerar_pdf(selecionados, dados_evento)
                st.success("PDF criado com sucesso!")
                st.balloons()

except Exception as e:
    st.error(f"Erro no aplicativo: {str(e)}")
    st.info("Por favor, acesse de um computador ou tente mais tarde.")
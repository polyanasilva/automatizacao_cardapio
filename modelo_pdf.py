from fpdf import FPDF

def gerar_pdf(dados, dados_evento):
    pdf = FPDF()
    
    # Pagina de capa
    pdf.add_page()
    pdf.image("assets/image1.png", x=0, y=0, w=210, h=297)

    # Pagina 2 - conteudo
    pdf.add_page()

    # 1. adiciona a logo no topo da pagina
    pdf.image("assets/image2.png", x=(210-60)/2, y=10, w=55, h=40)

    # move a posicao para baixo da logo para nao escrever por cima dela
    pdf.set_xy(10,60)
    
    # 2. Conteudo do cardapio
    pdf.set_font("Arial", size=10)

    # Informações básicas (agora usando os dados do formulário)
    pdf.cell(200, 10, txt=f"Estamos enviando proposta para {dados_evento['recepcao'].lower()}", ln=True)
    pdf.cell(200, 6, txt=f"Local: {dados_evento['local']}", ln=True)
    pdf.cell(200, 6, txt=f"Data: {dados_evento['data_evento']}", ln=True)
    pdf.cell(200, 6, txt=f"Número de convidados: {dados_evento['num_convidados']}", ln=True)
    pdf.cell(200, 6, txt=f"Horário: {dados_evento['horario']}", ln=True)
    
    # Cardápio
    pdf.ln(2)
    pdf.cell(200, 10, txt="O que iremos servir:", ln=True)

    for categoria, itens in dados.items():
        if itens:
            pdf.ln(1)
            pdf.set_font("Arial", 'B', 10)
            if categoria == "Finger Foods" or categoria == "Sobremesas":
                pdf.cell(200, 5, txt=f'{categoria}: (escolher 02 opções)', ln=True)
            elif categoria == "Prato Principal":
                pdf.cell(200, 5, txt=f'{categoria}: (escolher 03 opções)', ln=True)
            elif categoria == "Bebidas":
                pdf.cell(200, 5, txt=f'{categoria}: (02 tipos de sucos)', ln=True)
            else: 
                pdf.cell(200, 5, txt=f'{categoria}:', ln=True)

            pdf.set_font("Arial", size=10)
            for item in itens:
                pdf.cell(200, 5, txt=f" - {item}", ln=True)

    pdf.set_font("Arial", 'B')
    pdf.cell(200, 10, txt="Observação: Já está incluido garçons, copeira, todas as louças e transporte até o local.", ln=True)

    pdf.set_font("Arial")
    pdf.cell(200, 6, txt=f"- Valor: {dados_evento['valor']}", ln=True)

    pdf.cell(200, 6, txt="- Forma de pagamento 50% adiantado e os outros 50% até 48horas antes da festa. 05:00hs de evento.", ln=True)
    pdf.cell(200, 6, txt="- Não nos responsabilizamos pela alimentação dos fornecedores da festa.", ln=True)
    pdf.cell(200, 6, txt="- Validade da proposta: 30 dias.", ln=True)

    pdf.cell(200, 10, txt=f"Belém, {dados_evento['data_contrato']}.", ln=True)

    # 3. Adiciona a IMAGEM DO RODAPÉ no fim da página
    altura_rodape = 100
    y_pos = 297 - altura_rodape
    pdf.image("assets/image3.png", x=0, y=y_pos, w=210, h=altura_rodape)

    # Salvar PDF
    caminho = f"outputs/proposta_{dados_evento['recepcao'].lower()}.pdf"
    pdf.output(caminho)
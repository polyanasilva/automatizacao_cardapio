from fpdf import FPDF

def gerar_pdf(dados, dados_evento):
    pdf = FPDF()
    
    # Página de capa
    pdf.add_page()
    pdf.image("assets/image1.png", x=0, y=0, w=210, h=297)

    # Página 2 - conteúdo
    pdf.add_page()

    # Logo no topo
    pdf.image("assets/image2.png", x=(210-60)/2, y=10, w=55, h=40)

    # Posiciona abaixo da logo
    pdf.set_xy(10, 60)
    pdf.set_font("Arial", size=10)

    # Informações básicas
    pdf.cell(200, 10, txt=f"Estamos enviando proposta para {dados_evento['recepcao'].lower()}", ln=True)
    pdf.cell(200, 6, txt=f"Local: {dados_evento['local']}", ln=True)
    pdf.cell(200, 6, txt=f"Data: {dados_evento['data_evento']}", ln=True)
    pdf.cell(200, 6, txt=f"Número de convidados: {dados_evento['num_convidados']}", ln=True)
    pdf.cell(200, 6, txt=f"Horário: {dados_evento['horario']}", ln=True)

    pdf.ln(2)
    pdf.cell(200, 10, txt="O que iremos servir:", ln=True)

    for categoria, itens in dados.items():
        if itens:
            # Checa se precisa adicionar nova página
            if pdf.get_y() > 250:
                pdf.add_page()
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
                if pdf.get_y() > 270:
                    pdf.add_page()
                pdf.cell(200, 5, txt=f" - {item}", ln=True)

    # Observações
    pdf.ln(2)
    pdf.set_font("Arial", 'B')
    pdf.cell(200, 10, txt="Observação: Já está incluído garçons, copeira, todas as louças e transporte até o local.", ln=True)

    pdf.set_font("Arial")
    pdf.cell(200, 6, txt=f"- Valor: {dados_evento['valor']}", ln=True)
    pdf.cell(200, 6, txt="- Forma de pagamento 50% adiantado e os outros 50% até 48 horas antes da festa. 05:00hs de evento.", ln=True)
    pdf.cell(200, 6, txt="- Não nos responsabilizamos pela alimentação dos fornecedores da festa.", ln=True)
    pdf.cell(200, 6, txt="- Validade da proposta: 30 dias.", ln=True)
    pdf.cell(200, 10, txt=f"Belém, {dados_evento['data_contrato']}.", ln=True)

    # Posiciona rodapé 2 linhas após o texto ou no fim da página
    altura_rodape = 100
    espaco_para_respeitar = 2 * 6  # duas linhas de 6mm
    y_rodape = max(pdf.get_y() + espaco_para_respeitar, 297 - altura_rodape)

    # Se o rodapé ultrapassar a página, cria nova página
    if y_rodape + altura_rodape > 297:
        pdf.add_page()
        y_rodape = 297 - altura_rodape

    pdf.image("assets/image3.png", x=0, y=y_rodape, w=210, h=altura_rodape)

    # Salvar PDF
    caminho = f"outputs/proposta_{dados_evento['recepcao'].lower()}.pdf"
    pdf.output(caminho)

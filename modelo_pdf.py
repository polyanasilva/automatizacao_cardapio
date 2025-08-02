from fpdf import FPDF

def gerar_pdf(dados):
    pdf = FPDF()
    
    # Pagina de capa
    pdf.add_page()
    pdf.image("assets/image1.png", x=0, y=0, w=210, h=297)

    # Pagina 2 - conteudo
    pdf.add_page()

    # 1. adiciona a logo no topo da pagina
    pdf.image("assets/image2.png", x=(210-60)/2, y=10, w=55, h=40)

    # move a posicao para baixo da logo para nao escrever por cima dela
    pdf.set_xy(10,50)


    # 2. Conteudo do cardapio
    pdf.set_font("Times", size=12)

    for categoria, itens in dados.items():
        if itens:
            pdf.ln(10)
            pdf.set_font("Times", 'B', 14)
            pdf.cell(200, 10, txt=categoria, ln=True)
            pdf.set_font("Times", size=12)
            for item in itens:
                pdf.cell(200, 8, txt=f" - {item}", ln=True)





    # 3. Adiciona a IMAGEM DO RODAPÉ no fim da página
    # Altura da imagem: digamos que seja 25 mm
    altura_rodape = 100
    y_pos = 297 - altura_rodape  # 297 é a altura da página A4

    pdf.image("assets/image3.png", x=0, y=y_pos, w=210, h=altura_rodape)

    # Salvar PDF
    pdf.output("outputs/cardapio.pdf")


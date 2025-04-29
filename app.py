import streamlit as st
from docx import Document
from docx.shared import Pt
from datetime import datetime
import os

# Funzione per generare un nome di file univoco
def generate_unique_filename(nome_cliente):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f'{timestamp}_{nome_cliente}.docx'

# Funzione per aggiungere una linea vuota
def add_empty_line(paragraph, count=1):
    for _ in range(count):
        run = paragraph.add_run()
        run.add_break()

# Interfaccia utente con Streamlit
st.title('Generatore di Preventivi')

nome_cliente = st.text_input('Nome del Cliente')
tipo_sito = st.selectbox('Tipo di Sito', ['blog', 'e-commerce', 'portfolio', 'altro'])
piattaforma = st.selectbox('Piattaforma', ['WordPress', 'Codice Normale'])
seo = st.radio('SEO', ['si', 'no'])
hosting = st.radio('Hosting', ['si', 'no'])
altro_sito = st.text_input('Altri Siti', '')
descrizione_personalizzata = st.text_area('Descrizione Personalizzata')

if st.button('Genera Preventivo'):
    # Calcolo del preventivo
    costo_base = 500
    costo_piattaforma = 300 if piattaforma == "WordPress" else 600
    costo_sito = {
        'blog': 200,
        'e-commerce': 1000,
        'portfolio': 400,
        'altro': 600
    }.get(tipo_sito, 0)
    costo_seo = 200 if seo == "si" else 0
    costo_hosting = 100 if hosting == "si" else 0

    totale = costo_base + costo_piattaforma + costo_sito + costo_seo + costo_hosting

    # Creazione documento Word
    filename = generate_unique_filename(nome_cliente)
    document = Document()

    # Stile del preventivo (font e layout)
    style = document.styles['Normal']
    font = style.font
    font.name = 'Arial'
    font.size = Pt(10)

    # Intestazione cliente e data
    header = document.sections[0].header
    header_paragraph = header.paragraphs[0]
    header_paragraph.text = "Cliente: " + nome_cliente
    header_paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT

    header_paragraph = header.add_paragraph()
    header_paragraph.text = "Data: " + datetime.now().strftime("%d/%m/%Y")
    header_paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT

    # Preventivo titolo
    document.add_heading(f'Preventivo per {nome_cliente}', level=1)

    # Tabella preventivo
    table = document.add_table(rows=1, cols=4)
    table.style = 'Table Grid'

    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'Descrizione'
    hdr_cells[1].text = 'Quantità'
    hdr_cells[2].text = 'Prezzo'
    hdr_cells[3].text = 'Subtotale'

    # Riga 1
    row_cells = table.add_row().cells
    row_cells[0].text = 'Creazione sito ' + tipo_sito
    row_cells[1].text = '1'
    row_cells[2].text = f'{costo_sito}€'
    row_cells[3].text = f'{costo_sito}€'

    # Riga 2
    row_cells = table.add_row().cells
    row_cells[0].text = 'Piattaforma ' + piattaforma
    row_cells[1].text = '1'
    row_cells[2].text = f'{costo_piattaforma}€'
    row_cells[3].text = f'{costo_piattaforma}€'

    # Riga 3 (SEO)
    row_cells = table.add_row().cells
    row_cells[0].text = 'SEO'
    row_cells[1].text = '1'
    row_cells[2].text = f'{costo_seo}€'
    row_cells[3].text = f'{costo_seo}€'

    # Riga 4 (Hosting)
    row_cells = table.add_row().cells
    row_cells[0].text = 'Hosting'
    row_cells[1].text = '1'
    row_cells[2].text = f'{costo_hosting}€'
    row_cells[3].text = f'{costo_hosting}€'

    # Riga 5 (Descrizione personalizzata)
    if descrizione_personalizzata:
        row_cells = table.add_row().cells
        row_cells[0].text = descrizione_personalizzata
        row_cells[1].text = '1'
        row_cells[2].text = '0€'
        row_cells[3].text = '0€'

    # Aggiunta totale
    paragraph = document.add_paragraph()
    paragraph.add_run(f'Totale: {totale}€').bold = True
    paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT

    # Salva il documento
    document.save(filename)

    # Mostra il link per il download
    st.download_button(
        label="Scarica il Preventivo",
        data=open(filename, "rb").read(),
        file_name=filename,
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
import streamlit as st
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from datetime import datetime

def generate_doc(nome_cliente, tipo_sito, piattaforma, seo, hosting, altro_sito, descrizione_personalizzata):
    costo_base = 500
    costo_piattaforma = 300 if piattaforma == "WordPress" else 600
    costo_sito = {
        'blog': 200,
        'e-commerce': 1000,
        'portfolio': 400,
        'altro': 600
    }.get(tipo_sito, 0)
    costo_seo = 200 if seo else 0
    costo_hosting = 100 if hosting else 0

    totale = costo_base + costo_piattaforma + costo_sito + costo_seo + costo_hosting

    document = Document()
    style = document.styles['Normal']
    font = style.font
    font.name = 'Arial'
    font.size = Pt(10)

    document.add_heading(f'Preventivo per {nome_cliente}', level=1)

    table = document.add_table(rows=1, cols=4)
    table.style = 'Table Grid'
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'Descrizione'
    hdr_cells[1].text = 'Quantità'
    hdr_cells[2].text = 'Prezzo'
    hdr_cells[3].text = 'Subtotale'

    def add_row(desc, prezzo):
        row = table.add_row().cells
        row[0].text = desc
        row[1].text = '1'
        row[2].text = f'{prezzo}€'
        row[3].text = f'{prezzo}€'

    add_row(f'Creazione sito {tipo_sito}', costo_sito)
    add_row(f'Piattaforma {piattaforma}', costo_piattaforma)
    add_row('SEO', costo_seo)
    add_row('Hosting', costo_hosting)
    if descrizione_personalizzata:
        add_row(descrizione_personalizzata, 0)

    document.add_paragraph(f'Totale: {totale}€').alignment = WD_ALIGN_PARAGRAPH.RIGHT

    filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{nome_cliente}.docx"
    document.save(filename)
    return filename

# Streamlit UI
st.title("Generatore di Preventivi Web")

with st.form("preventivo_form"):
    nome_cliente = st.text_input("Nome cliente")
    tipo_sito = st.selectbox("Tipo di sito", ["blog", "e-commerce", "portfolio", "altro"])
    piattaforma = st.radio("Piattaforma", ["WordPress", "Codice personalizzato"])
    seo = st.checkbox("Ottimizzazione SEO")
    hosting = st.checkbox("Include Hosting")
    altro_sito = st.text_input("Specificare se 'altro'")
    descrizione = st.text_area("Descrizione personalizzata")

    submitted = st.form_submit_button("Genera Preventivo")

if submitted:
    filename = generate_doc(nome_cliente, tipo_sito, piattaforma, seo, hosting, altro_sito, descrizione)
    with open(filename, "rb") as file:
        st.download_button("Scarica il preventivo", file, file_name=filename)
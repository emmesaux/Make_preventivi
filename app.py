from flask import Flask, render_template, request, send_file
from docx import Document
from datetime import datetime
import os

app = Flask(__name__, template_folder='templates')
app.secret_key = 'chiave_segreta'

# Funzione per generare un nome di file univoco
def generate_unique_filename(nome_cliente):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f'{timestamp}_{nome_cliente}.docx'

@app.route('/')
def index():
    return render_template('preventivo.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        nome_cliente = request.form.get('nomeCliente')
        tipo_sito = request.form.get('tipoSito')
        piattaforma = request.form.get('piattaforma')
        seo = request.form.get('seo')
        hosting = request.form.get('hosting')
        descrizione = request.form.get('descrizione')
        specifica_altro = request.form.get('specificaAltro')

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
        document.add_heading(f'Preventivo per {nome_cliente}', level=1)
        document.add_paragraph(f'Tipo di sito: {tipo_sito}')
        if tipo_sito == 'altro' and specifica_altro:
            document.add_paragraph(f'Specifica del sito: {specifica_altro}')
        document.add_paragraph(f'Piattaforma: {piattaforma}')
        document.add_paragraph(f'SEO: {"Incluso" if seo == "si" else "Non incluso"}')
        document.add_paragraph(f'Gestione Hosting: {"Inclusa" if hosting == "si" else "Non inclusa"}')
        document.add_paragraph(f'Totale: €{totale}')
        
        # Aggiunta della grafica di personalizzazione e descrizione
        document.add_paragraph('---')
        document.add_paragraph('Descrizione del progetto:')
        document.add_paragraph(descrizione)
        document.add_paragraph('Personalizzazione grafica inclusa nel progetto.')
        document.save(filename)

        # Invia il file generato
        return send_file(filename, as_attachment=True)

port = int(os.environ.get('PORT', 8000))
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)

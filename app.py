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
        # Dati dal form
        nome_cliente = request.form.get('nomeCliente')
        tipo_sito = request.form.get('tipoSito')
        specifica_altro = request.form.get('specificaAltro', '')
        piattaforma = request.form.get('piattaforma')
        seo = request.form.get('seo')
        hosting = request.form.get('hosting')
        descrizione = request.form.get('descrizione')

        # Costi personalizzati dal form
        costo_base = float(request.form.get('costoBase', 500))
        costo_wordpress = float(request.form.get('costoWordpress', 300))
        costo_codice = float(request.form.get('costoCodice', 600))
        costo_seo = float(request.form.get('costoSeo', 200)) if seo == "si" else 0
        costo_hosting = float(request.form.get('costoHosting', 100)) if hosting == "si" else 0

        # Costi tipo sito
        costo_sito = {
            'blog': float(request.form.get('costoBlog', 200)),
            'e-commerce': float(request.form.get('costoEcommerce', 1000)),
            'portfolio': float(request.form.get('costoPortfolio', 400)),
            'altro': float(request.form.get('costoAltro', 600))
        }.get(tipo_sito, 0)

        # Determina il costo della piattaforma
        costo_piattaforma = costo_wordpress if piattaforma == "WordPress" else costo_codice

        # Calcolo totale
        totale = costo_base + costo_piattaforma + costo_sito + costo_seo + costo_hosting

        # Creazione documento Word
        filename = generate_unique_filename(nome_cliente)
        document = Document()
        document.add_heading(f'Preventivo per {nome_cliente}', level=1)
        document.add_paragraph(f'Tipo di sito: {tipo_sito.capitalize()}' + (f' ({specifica_altro})' if tipo_sito == 'altro' else ''))
        document.add_paragraph(f'Piattaforma: {piattaforma}')
        document.add_paragraph(f'SEO: {"Incluso" if seo == "si" else "Non incluso"}')
        document.add_paragraph(f'Gestione Hosting: {"Incluso" if hosting == "si" else "Non incluso"}')
        document.add_paragraph(f'Descrizione del progetto: {descrizione}')
        document.add_paragraph(f'Totale: €{totale}')

        document.save(filename)

        # Invia il file generato
        return send_file(filename, as_attachment=True)

port = int(os.environ.get('PORT', 8000))
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)

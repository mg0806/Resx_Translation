from flask import Flask, render_template, request, redirect, send_file
import xml.etree.ElementTree as ET
from googletrans import Translator
import os

app = Flask(__name__)
translator = Translator()

def translate_resx(file_path, target_language):
    tree = ET.parse(file_path)
    root = tree.getroot()

    for data in root.findall('data'):
        name = data.get('name')
        if name:
            try:
                translation = translator.translate(name, src='en', dest=target_language).text
            except Exception as e:
                print(f"Error translating '{name}': {e}")
                continue

            value_element = data.find('value')
            if value_element is None:
                value_element = ET.SubElement(data, 'value')
            value_element.text = translation

    translated_file_path = os.path.splitext(file_path)[0] + ".resx"
    tree.write(translated_file_path)
    return translated_file_path

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        language_code = request.form['language']
        file = request.files['file']
        if file:
            file_path = os.path.join('uploads', file.filename)
            file.save(file_path)

            translated_file = translate_resx(file_path, language_code)
            return send_file(translated_file, as_attachment=True)

    return render_template('index.html')

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True)

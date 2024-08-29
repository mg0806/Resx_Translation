from flask import Flask, render_template, request, redirect, send_file
import xml.etree.ElementTree as ET
from googletrans import Translator
import os
import re

app = Flask(__name__)
translator = Translator()

def get_culture_code(language):
    # A dictionary to map language codes to culture codes
    language_to_culture = {
        'fr': 'fr-FR',
        'es': 'es-ES',
        'de': 'de-DE',
        'en': 'en-US',
        'pt': 'pt-PT'  # European Portuguese
        # Add more mappings as needed
    }
    
    # Return the corresponding culture code, default to language.lower() + "-" + language.upper()
    return language_to_culture.get(language, f"{language.lower()}-{language.upper()}")

def translate_resx(file_path, target_language):
    # Parse the file
    tree = ET.parse(file_path)
    root = tree.getroot()

    for data in root.findall('data'):
        value_element = data.find('value')
        if value_element is not None and value_element.text:
            try:
                translation = translator.translate(value_element.text, src='en', dest=target_language).text
            except Exception as e:
                print(f"Error translating '{value_element.text}': {e}")
                translation = value_element.text  # Fallback to original text

            value_element.text = translation

    # Get the culture code based on the target language
    culture_code = get_culture_code(target_language)

    # Modify the filename to include the culture code
    base, ext = os.path.splitext(file_path)
    # Regex pattern to find the current language code in the filename
    pattern = re.compile(r'\.[a-z]{2}-[A-Z]{2}\.resx$')
    # Replace with the new culture code
    translated_file_path = pattern.sub(f'.{culture_code}.resx', base + ext)

    # If no existing language code pattern is found, append the new culture code
    if translated_file_path == file_path:
        translated_file_path = f"{base}.{culture_code}.resx"

    tree.write(translated_file_path, encoding='utf-8', xml_declaration=True)
    return translated_file_path

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        language_code = request.form.get('language', 'en')
        file = request.files.get('file')
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

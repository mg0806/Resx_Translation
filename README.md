RESX File Translator
Overview
The RESX File Translator is a Flask-based web application that allows users to upload .resx files and translate the content from English to various languages. The application utilizes the Google Translate API to provide translations and stores the translated content in the value field of the .resx file.

Features
Upload .resx files for translation.
Select target languages (e.g., French, Spanish, German, Portuguese).
Download the translated .resx file with the appropriate culture code.
Live Demo
You can use the live application at:

manohargupta.pythonanywhere.com

Installation
To run this project locally, follow these steps:

Clone the Repository:

bash
Copy code
git clone <repository-url>
cd <repository-directory>
Set Up Virtual Environment (optional but recommended):

bash
Copy code
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
Install Dependencies:

bash
Copy code
pip install Flask googletrans==4.0.0-rc1
Run the Application:

bash
Copy code
python app.py
Access the Application: Open your web browser and go to http://127.0.0.1:5000 to use the application.

Usage
Navigate to the homepage of the application.
Select the target language from the dropdown menu.
Upload your .resx file using the file upload field.
Click the "Translate" button.
Once the translation is complete, the translated .resx file will be automatically downloaded.
File Format
The .resx file should contain elements structured like this:

xml
Copy code
<data name="Hello" xml:space="preserve">
    <value />
</data>
The application will translate the name attributes into the specified target language and store the translations in the corresponding value fields.

Troubleshooting
Ensure that your .resx file follows the proper XML structure. Any malformed XML may cause the translation to fail.
If you encounter issues with the Google Translate API, make sure your API credentials are correctly configured (if applicable).

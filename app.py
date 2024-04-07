import pandas as pd
import clean_helper as c
import sqlite3
from flask import Flask, jsonify, request
from flasgger import Swagger, LazyString, LazyJSONEncoder, swag_from

DB_FILE = 'db/text_clean.db'

app = Flask(__name__)

app.json_encoder = LazyJSONEncoder
swagger_template = dict(
info = {
    'title': 'API Documentation for Data Cleansing',
    'version': '1.0.0',
    'description': 'Dokumentasi API untuk Data Cleansing',
    }
    # host = LazyString(lambda: request.host)
)
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'docs',
            "route": '/docs.json',
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs/"
}
swagger = Swagger(app, template=swagger_template,             
                  config=swagger_config)

@app.route('/', methods=['GET'])
def hello_world():
    return 'Welcome to Data Cleansing Project.<br/><br/> <b>created by: hendrihmwn</b>'

@swag_from("docs/text_clean.yml", methods=['POST'])
@app.route('/text-clean', methods=['POST'])
def text_clean():
    # required validation
    if 'text' not in request.form:
        return res('text is required', 400)
    
    text = request.form['text']
    # clean processing
    text_clean = c.clean(text)
    # replacing word
    kamus = c.kamus_alay()
    text_clean = c.word_substitute(text_clean, kamus)

    # save db
    data = [(text_clean, text)]
    insert_into_texts(data)
    
    return res({
        "text_raw": text,
        "text_clean": text_clean
        })

@swag_from("docs/text_upload.yml", methods=['POST'])
@app.route('/text-upload', methods=['POST'])
def text_upload():
    # required validation
    if 'file' not in request.files:
        return res('file is required', 400)
    
    file = request.files.getlist('file')[0]
    df = pd.read_csv(file)
    texts = df.text.to_list()
    # read kamus for replacing word
    kamus = c.kamus_alay()

    cleaned_text = []
    data_insert = []
    for text in texts:
        # clean processing
        text_clean = c.clean(text)
        text_clean = c.word_substitute(text_clean, kamus)
        cleaned_text.append({
            "text_raw": text,
            "text_clean": text_clean
        })
        data_insert.append((text_clean, text))

    # save db
    insert_into_texts(data_insert)
    return res(cleaned_text)

def res(data, code = 200):
    return jsonify({
        "status_code": code,
        "data": data
    }), code

def insert_into_texts(data):
    conn = sqlite3.connect(DB_FILE)
    try:
        conn.cursor().executemany("INSERT INTO texts (text_clean, text_raw) VALUES (?, ?)", data)
        conn.commit()
        print ("success insert to texts")
    except sqlite3.Error as e:
        conn.rollback()
        print ("failed insert to texts", str(e))
    conn.cursor().close()
    conn.close()

if __name__ == '__main__':
    app.run()
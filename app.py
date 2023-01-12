from project.data_cruncher import process_entity
from project.data_models import FormData
from flask import Flask, send_from_directory, request
import dataclasses_jsonschema
import os.path

app = Flask(__name__)
assets_folder = os.path.join(app.root_path, 'static')


@app.route('/')
def get_home():
  filename = "index.html"
  return send_from_directory(assets_folder+"/views/", filename)


@app.route('/hello')
def hello():
  return "Hello World!"


@app.route('/static/<path>:path')
def get_static_file(path):
  return send_from_directory(assets_folder, path)


@app.route('/data', methods=['POST'])
def post_data():
  try:
    form_data = FormData.from_dict(request.json)
    print("IN METHOD1")
    #process_entity(form_data)
    return form_data.to_json()
  except dataclasses_jsonschema.ValidationError as e:
    return str(e), 500


if __name__ == 'main':
  app.run()

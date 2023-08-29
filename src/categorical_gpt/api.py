import os

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from .cgpt import CategoricalGPT
from .openai_driver import OpenAIDriver
from .ordering import ordered_options
from .coloring import color_coding
from .embedding import make_mds_embedding

api = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'gui', '.output', 'public'))
CORS(api)

driver_mappings = {
    'gpt-3.5-turbo': OpenAIDriver(api_key=os.environ.get('OPENAI_API_KEY'), cache_path=os.environ.get('CACHE_PATH')),
    'gpt-4': OpenAIDriver(api_key=os.environ.get('OPENAI_API_KEY'), cache_path=os.environ.get('CACHE_PATH'))
}


def error(message):
    return jsonify(
        {
            "error": True,
            "message": message
        }
    )


def make_cgpt():
    category_name = request.json.get('category_name', '')
    category_options = request.json.get('category_options', '')

    if category_name == '' or category_options == '':
        return error('Specify a category name and options.')

    model = request.json.get('model', '')
    llm_driver = driver_mappings[model]
    if llm_driver is None:
        return error('Model not mapped to a driver')

    cgpt = CategoricalGPT(llm_driver, category_name, category_options)

    return cgpt


@api.route('/api/load-characteristics', methods=['POST'])
def load_characteristics():
    model_params = request.json.get('model_params', {})
    cgpt = make_cgpt()
    cgpt.get_characteristics(capitalized=True, **model_params)
    return jsonify(cgpt.structure())


@api.route('/api/load-heuristic', methods=['POST'])
def load_heuristic():
    model_params = request.json.get('model_params')
    characteristic = request.json.get('characteristic', None)
    if characteristic is None:
        return error('Characteristic needs to be specified.')
    cgpt = make_cgpt()
    cgpt.get_heuristic(characteristic=characteristic, **model_params)
    return jsonify(cgpt.structure())


@api.route('/api/load-values', methods=['POST'])
def load_values():
    model_params = request.json.get('model_params')
    characteristic = request.json.get('characteristic', None)
    heuristic = request.json.get('heuristic', None)
    if characteristic is None or heuristic is None:
        return error('Characteristic and heuristic needs to be specified.')
    cgpt = make_cgpt()
    cgpt.apply_heuristic(characteristic=characteristic, heuristic=heuristic, **model_params)
    return jsonify(cgpt.structure())


@api.route('/api/load-results', methods=['POST'])
def load_results():
    structure = request.json.get('structure')
    ordering_method = request.json.get('ordering_method', 'tsp+mds')
    cgpt = make_cgpt()
    cgpt.update_from_structure(structure)
    return jsonify(
        {
            'ordering': ordered_options(cgpt, ordering_method=ordering_method),
            'color_coding': color_coding(cgpt, decimals=4),
            'embedding': make_mds_embedding(cgpt, tolist=True)[0],
            'feature_vectors_dict': cgpt.make_feature_vectors(as_dict=True),
            'feature_vectors': cgpt.make_feature_vectors(as_dict=False)
        }
    )


@api.route('/api/load-ordering', methods=['POST'])
def load_ordering():
    structure = request.json.get('structure')
    ordering_method = request.json.get('ordering_method', 'tsp+mds')
    cgpt = make_cgpt()
    cgpt.update_from_structure(structure)
    return jsonify(
        {
            'ordering': ordered_options(cgpt, ordering_method=ordering_method),
        }
    )


@api.route('/', defaults={'path': ''})
@api.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(api.static_folder + '/' + path):
        if path in ['characteristics', 'value-assignments', 'results', 'export']:
            return send_from_directory(api.static_folder, os.path.join(path, 'index.html'))
        return send_from_directory(api.static_folder, path)
    else:
        return send_from_directory(api.static_folder, 'index.html')

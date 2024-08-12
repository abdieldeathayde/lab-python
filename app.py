#!/usr/bin/python
from flask import Flask, jsonify, abort, make_response, request, url_for
from flask_httpauth import HTTPBasicAuth 

auth = HTTPBasicAuth()
app = Flask(__name__)

livros = [
    {'id': 1, 'titulo': 'Linguagem de Programacao C', 'autor': 'Dennis Ritchie'},
    {'id': 2, 'titulo': 'Java como programar', 'autor': 'Deitel & Deitel'}
]

@app.route('/livros', methods=['GET'])
def obtem_livros():
    return jsonify({'livros': livros})

@app.route('/livros/<int:idLivro>', methods=['GET'])
def detalhe_livro(idLivro):
    resultado = [resultado for resultado in livros if resultado['id'] == idLivro]
    if len(resultado) == 0:
        abort(404)
    return jsonify({'livro': resultado[0]})

@app.route('/livros/<int:idLivro>', methods=['DELETE'])
def excluir_livro(idLivro):
    resultado = [resultado for resultado in livros if resultado['id'] == idLivro]
    if len(resultado) == 0:
        abort(404)
    livros.remove(resultado[0])
    return jsonify({'resultado': True})

@app.route('/livros', methods=['POST'])
def criar_livro():
    if not request.json or not 'titulo' in request.json:
        abort(400)
    livro = {
        'id': livros[-1]['id'] + 1,
        'titulo': request.json['titulo'],
        'autor': request.json.get('autor', "")
    }
    livros.append(livro)
    return jsonify({'livro': livro}), 201

@app.route('/livros/<int:idLivro>', methods=['PUT'])
def atualizar_livro(idLivro):
    resultado = [resultado for resultado in livros if resultado['id'] == idLivro]
    if len(resultado) == 0:
        abort(404)
    if not request.json:
        abort(400)
    resultado[0]['titulo'] = request.json.get('titulo', resultado[0]['titulo'])
    resultado[0]['autor'] = request.json.get('autor', resultado[0]['autor'])
    return jsonify({'livro': resultado[0]})

@auth.get_password
def get_password(username):
    if username == 'aluno':
        return 'senha123'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'erro': 'Acesso Negado'}), 403)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'erro': 'Recurso Nao encontrado'}), 404)

if __name__ == "__main__":
    print("Servidor no ar!")
    app.run(debug=True)

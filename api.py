from flask import Flask, jsonify, request
import bancoDeDados
import sha256
app = Flask(__name__)

#api em flask que a partir dessa rota seleciona
@app.route('/api/hash', methods=['GET', 'POST'])
def hash():
    # Uso do GET penso que não será necessario, só o coloquei como forma de testar se o banco de dados estava funcionando
    #caso achem alguma funcionalidade para ele, podem usar tranquilamente
    if request.method == 'GET':
        dados_do_banco = bancoDeDados.selecionar_hash_do_banco("1")
        # Dicionário com o hash
        dados = {'id': dados_do_banco[0], 'hash': dados_do_banco[1]} if dados_do_banco !=None else {"msg" : "Dados não encontrados", "hash" : None}
        # Retornar os dados como JSON
        return jsonify(dados)
    
    # Metodo post vai ser o principal metodo do nosso projeto
    if request.method == 'POST':
        # Obter o hash do corpo da requisição
        dados_recebidos = request.json
        arquivo = dados_recebidos.get('arquivo')
        #assim que conseguirmos os dados do usuario, penso que eles serão tratados em uma função e trazidos de volta para API
        #esse tratamento de arquivo viria já sendo um hash
        novo_hash = sha256.codificar_arquivo_em_sha256(arquivo)

        # verifica se o hash que está no banco de dados
        dados_do_banco = bancoDeDados.selecionar_hash_do_banco(novo_hash)

        # caso não exista, insere no banco
        if(dados_do_banco == None):
            bancoDeDados.adicionar_valores(novo_hash)
            return jsonify({'mensagem': 'Hash inserido com sucesso.'})
        #caso exista, mande uma mensagem via json dizendo que já existe esse hash no banco
        else:
            return jsonify({'mensagem': 'Hash já existente no banco de dados'})
           

        
        

app.run(debug=True)


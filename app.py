from flask import Flask, render_template, request, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
from wtforms.validators import InputRequired
import bancoDeDados
import os
from calc_hash import calcular_hash_arquivo, limpar_diretorio_verificacao

app = Flask(__name__)
app.config['SECRET_KEY'] = 'v6Fre$zu7ZJHfcMn356#8c'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['VERIF_FOLDER'] = 'uploads_verificacao'

# Verifica se o diretório de upload existe, se não, cria
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])
    
if not os.path.exists(app.config['VERIF_FOLDER']):
    os.makedirs(app.config['VERIF_FOLDER'])


class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")

@app.route('/', methods=['GET',"POST"])
@app.route('/home', methods=['GET',"POST"])
def home():
    return render_template('index.html')

@app.route('/registro', methods=['GET',"POST"])
def registro():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data   # Variável que vai armazenar o arquivo
        print(file.filename)    # Só pra testar se tá chegando certo... E talvez pra verificar que tipo de arquivo é
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
        file.save(filepath)
        # A instância do método para a transformação do arquivo em Hash deve ser colocado aqui!
        hash = calcular_hash_arquivo(filepath) # arquivo já transformado em hash

        bancoDeDados.adicionar_valores(hash) #método que adiciona o hash ao banco de dados
        return render_template('registrado.html')
    return render_template('registro.html', form=form)
    
@app.route('/validacao', methods=['GET',"POST"])
def validacao():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data   # Variável que vai armazenar o arquivo
        print(file.filename)    # Só pra testar se tá chegando certo... E talvez pra verificar que tipo de arquivo é
        filepath = os.path.join(app.config['VERIF_FOLDER'], secure_filename(file.filename))
        file.save(filepath)
        # A instância do método para a transformação do arquivo em Hash deve ser colocado aqui!
        hash = calcular_hash_arquivo(filepath) # arquivo já transformado em hash

        resultado_banco =  bancoDeDados.selecionar_hash_do_banco(hash) #método para verificar se o hash existe ou não no banco, caso não exista retorna um None
        resultado = "Válido" if resultado_banco != None else "Inválido" #verifica se o valor retornado do banco é válido ou não

        limpar_diretorio_verificacao()

        return render_template('resultado.html', resultado=resultado)
    return render_template('validacao.html', form=form)
    
if __name__ == '__main__':
    app.run()
from flask import Flask, render_template, request, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
from wtforms.validators import InputRequired
import bancoDeDados

app = Flask(__name__)
app.config['SECRET_KEY'] = 'v6Fre$zu7ZJHfcMn356#8c'

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
        # A instância do método para a transformação do arquivo em Hash deve ser colocado aqui!
        hash = ("método para transformação em hash") # arquivo já transformado em hash

        bancoDeDados.adicionar_valores(hash) #método que adiciona o hash ao banco de dados
        return render_template('registrado.html')
    return render_template('registro.html', form=form)
    
@app.route('/validacao', methods=['GET',"POST"])
def validacao():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data   # Variável que vai armazenar o arquivo
        print(file.filename)    # Só pra testar se tá chegando certo... E talvez pra verificar que tipo de arquivo é
        # A instância do método para a transformação do arquivo em Hash deve ser colocado aqui!
        hash = ("método para transformação em hash") # arquivo já transformado em hash
        
        resultado_banco =  bancoDeDados.selecionar_hash_do_banco(hash) #método para verificar se o hash existe ou não no banco, caso não exista retorna um None
        resultado = "Válido" if resultado_banco != None else "Inválido" #verifica se o valor retornado do banco é válido ou não
        return render_template('resultado.html', resultado=resultado)
    return render_template('validacao.html', form=form)
    
if __name__ == '__main__':
    app.run()
from flask import Flask, render_template, request, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
from wtforms.validators import InputRequired

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
        # A instância do método para o registro do Hash no Banco de Dados deve ser colocado aqui!
        return render_template('registrado.html')
    return render_template('registro.html', form=form)
    
@app.route('/validacao', methods=['GET',"POST"])
def validacao():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data   # Variável que vai armazenar o arquivo
        print(file.filename)    # Só pra testar se tá chegando certo... E talvez pra verificar que tipo de arquivo é
        # A instância do método para a transformação do arquivo em Hash deve ser colocado aqui!
        # A instância do método para verificação no banco de dados deve ser feita aqui!
        resultado = "Inserir resposta aqui" # De acordo com o resultado da verificação, essa string deve ser trocado para "Válido" ou "Inválido"
        return render_template('resultado.html', resultado=resultado)
    return render_template('validacao.html', form=form)
    
if __name__ == '__main__':
    app.run()
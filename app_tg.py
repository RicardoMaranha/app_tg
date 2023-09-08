from flask import Flask, render_template, request, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'cecilia'


app.config['SQLALCHEMY_DATABASE_URI'] = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGBD = 'mysql+mysqlconnector',
        usuario = 'root',
        senha = '123456',
        servidor = 'localhost',
        database = 'banco_tg'
    )

db = SQLAlchemy(app)

class Fornecedores(db.Model):
    id_fornecedor = db.Column(db.Interger, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    cnpj = db.Column(db.String(18), nullable=False)
    cep = db.Column(db.String(10))
    cidade = db.Column(db.String(100))
    estado = db.Column(db.String(50))
    rua = db.Column(db.String(255))
    numero = db.Column(db.Interger)
    telefone = db.Column(db.String(50))
    email = db.Column(db.String(50))

    def __repl__(self):
        return '<NAME %r>' % self.name


class Usuarios(db.Model):
    nickname = db.Column(db.string(50), primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    senha = db.Column(db.String(100), nullable=False)

    def __repl__(self):
        return '<NAME %r>' % self.name



@app.route('/')
def inicio():
    return render_template('index.html')

@app.route('/listaFornecedor')
def listaFornecedor():
    lista_fornecedores = Fornecedores.query.order_by(Fornecedores.id_fornecedor)
    return render_template('listaFornecedor.html', fornecedores = lista_fornecedores)

@app.route('/cadastraFornecedor')
def cadastraFornecedor():
    return render_template('cadastraFornecedor.html')

@app.route('/criarFornecedor', methods=['POST',])
def criarFornecedor():
    cnpj = request.form['cnpj']
    nome = request.form['nome']
    endereco = request.form['endereco']
    telefone = request.form['telefone']
    email = request.form['email']
    fornecedor = Fornecedor(cnpj,nome,endereco,telefone,email)
    lista_fornecedor.append(fornecedor)
    return redirect('/listaFornecedor')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/autenticar', methods=['POST',])
def autenticar():
    if 'admin' == request.form['senha']:
        session['usuario_logado'] = request.form['usuario']
        flash(session['usuario_logado'] + 'Usuário logado com sucesso')
        return redirect('/')
    else:
        flash('Usuario não logado')
        return redirect('/login')
    

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso!')
    return redirect('/') 


app.run(debug=True)

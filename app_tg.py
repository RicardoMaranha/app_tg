from flask import Flask, render_template, request, redirect, session, flash

app = Flask(__name__)
app.secret_key = 'cecilia'


class Cliente:
    def __init__(self, documento, nome, sobrenome, endereco, telefone, email, id_usuario, senha_usuario, id_cliente):
        self.documento = documento
        self.nome = nome
        self.sobrenome = sobrenome
        self.endereco = endereco
        self.telefone = telefone
        self.email = email
        self.id_usuario = id_usuario
        self.senha_usuario = senha_usuario
        self.id_cliente = id_cliente
        self.pedidos = []


class Fornecedor:
    def __init__(self, cnpj, nome, endereco, telefone, email):
        self.cnpj = cnpj
        self.nome = nome
        self.endereco = endereco
        self.telefone = telefone
        self.email = email
     

class Usuario:
    def __init__(self,nome,nickname, senha):
        self.nome = nome
        self.nickname = nickname
        self.senha = senha


usuario1 = Usuario("Ricardo","rickmaranha", "maranha" )
usuario2 = Usuario("Cecília", "ceciliamaranha", "mariaclara")
lista_fornecedor = []


@app.route('/')
def inicio():
    return render_template('index.html')

@app.route('/listaFornecedor')
def listaFornecedor():
    return render_template('listaFornecedor.html', fornecedores = lista_fornecedor)

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

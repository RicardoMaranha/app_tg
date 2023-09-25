from flask import render_template, request, redirect, session, flash, url_for
from app_tg import app, db
from models import Fornecedores, Usuarios

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
    cep = request.form['cep']
    cidade = request.form['cidade']
    estado = request.form['estado']
    rua = request.form['rua']
    numero = request.form['numero']
    telefone = request.form['telefone']
    email = request.form['email']

    fornecedor = Fornecedores.query.filter_by(nome).first()

    if fornecedor:
        flash('Fornecedor já cadastrado!')
        return redirect(url_for('listaFornecedor'))
    
    novo_fornecedor = Fornecedores(cnpj=cnpj, nome=nome,cep=cep,cidade=cidade,estado=estado,rua=rua,numero=numero,telefone=telefone,email=email)
    db.session.add(novo_fornecedor)
    db.session.commit()

    return redirect(url_for('listaFornecedor'))

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
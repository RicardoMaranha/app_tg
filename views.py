from flask import render_template, request, redirect, session, flash, url_for
from app_tg import app, db
from models import Fornecedores, Usuarios, Clientes

# Rotas Pagina Inicial
@app.route('/')
def inicio():
    return render_template('index.html', titulo='Editar Fornecedores')

# Rotas Login e Logout
@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)

@app.route('/autenticar', methods=['POST', 'GET', ])
def autenticar():
    usuario = Usuarios.query.filter_by(nickname=request.form['usuario']).first()
    if usuario:
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.nickname
            flash(usuario.nickname + ' logado com sucesso!')
            proxima_pagina = request.args.get('proxima')
            if proxima_pagina:
                return redirect(proxima_pagina)  # Redireciona para a rota de destino
            else:
                return redirect('/')  # Redireciona para a página padrão se 'proxima' não estiver presente


    else:
        flash('Usuario não logado')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso!')
    return redirect('/')

# Rota Listar Fornecedores
@app.route('/listaFornecedor')
def listaFornecedor():
    lista_fornecedores = Fornecedores.query.order_by(Fornecedores.id_fornecedor)
    return render_template('listaFornecedor.html',titulo='Lista de Fornecedores', fornecedores = lista_fornecedores)

# Rotas Para Cadastro de Fornecedor
@app.route('/cadastraFornecedor2')
def cadastraFornecedor2():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('cadastraFornecedor2')))
    return render_template('cadastraFornecedor2.html')

@app.route('/criarFornecedor', methods=['POST', ])
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

    fornecedor = Fornecedores.query.filter_by(nome=nome).first()

    if fornecedor:
        flash('Fornecedor já cadastrado!')
        return redirect(url_for('listaFornecedor'))

    novo_fornecedor = Fornecedores(cnpj=cnpj, nome=nome, cep=cep, cidade=cidade, estado=estado, rua=rua, numero=numero,
                                   telefone=telefone, email=email)
    db.session.add(novo_fornecedor)
    db.session.commit()

    return redirect(url_for('listaFornecedor'))

# Rota Atualizar Fornecedor
@app.route('/editarFornecedor/<int:id_fornecedor>')
def editarFornecedor(id_fornecedor):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login',proxima=url_for('editarFornecedor')))
    fornecedor = Fornecedores.query.filter_by(id_fornecedor=id_fornecedor).first()
    return render_template("editarFornecedor.html", fornecedor=fornecedor, titulo='Editar Fornecedor')

@app.route('/atualizarFornecedor', methods=['POST',])
def atualizarFornecedor():
    fornecedor = Fornecedores.query.filter_by(id_fornecedor=request.form['id_fornecedor']).first()
    fornecedor.cnpj = request.form['cnpj']
    fornecedor.nome = request.form['nome']
    fornecedor.cep = request.form['cep']
    fornecedor.cidade = request.form['cidade']
    fornecedor.estado = request.form['estado']
    fornecedor.rua = request.form['rua']
    fornecedor.numero = request.form['numero']
    fornecedor.telefone = request.form['telefone']
    fornecedor.email = request.form['email']

    db.session.add(fornecedor)
    db.session.commit()

    return redirect(url_for('listaFornecedor'))

# Rota Excluir
@app.route('/excluirFornecedor/<int:id_fornecedor>')
def excluirFornecedor(id_fornecedor):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))

    Fornecedores.query.filter_by(id_fornecedor=id_fornecedor).delete()
    db.session.commit()
    flash('Fornecedor exluido com sucesso!')
    return redirect(url_for('listaFornecedor'))


@app.route('/listaCliente')
def listaCliente():
    lista_cliente = Clientes.query.order_by(Clientes.id_cliente)
    return render_template('listaCliente.html', titulo='Lista de Clientes', clientes=lista_cliente)

@app.route('/cadastraCliente')
def cadastraCliente():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('cadastraCliente')))
    return render_template('cadastraCliente.html', titulo='Cadastrar Cliente')


@app.route('/criarCliente', methods=['POST', ])
def criarCliente():
    documento = request.form['documento']
    nome = request.form['nome']
    cep = request.form['cep']
    cidade = request.form['cidade']
    estado = request.form['estado']
    rua = request.form['rua']
    numero = request.form['numero']
    telefone = request.form['telefone']
    email = request.form['email']

    cliente = Clientes.query.filter_by(nome=nome).first()

    if cliente:
        flash('Cliente já cadastrado!')
        return redirect(url_for('listaCliente'))

    novo_cliente = Clientes(documento=documento, nome=nome, cep=cep, cidade=cidade, estado=estado, rua=rua, numero=numero,
                                   telefone=telefone, email=email)
    db.session.add(novo_cliente)
    db.session.commit()

    return redirect(url_for('listaCliente'))
from flask import render_template, request, redirect, session, flash, url_for
from app_tg import app, db
from models import Fornecedores, Usuarios, Clientes, MateriaPrima, EstoqueMateriaPrima
from helpers import FormUsuario, FormFornecedores, FormCadastraMateriaPrima, FormClientes, EstoqueMateriaPrimaForm
from datetime import datetime

# Rotas Pagina Inicial
@app.route('/')
def inicio():
    return redirect(url_for('login'))

# Rotas Login e Logout
@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    form = FormUsuario()
    return render_template('login.html', proxima=proxima,titulo='Login', form=form)

#Rotas para autenticar Usuário
@app.route('/autenticar', methods=['POST', 'GET', ])
def autenticar():
    form = FormUsuario()
    usuario = Usuarios.query.filter_by(nickname=form.nickname.data).first()
    if usuario:
        if form.senha.data == usuario.senha:
            session['usuario_logado'] = usuario.nickname
            flash(usuario.nickname + ' logado com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)  # Redireciona para a rota de destino
        else:
            return redirect(url_for('login'))  # Redireciona para a página padrão se 'proxima' não estiver presente

    else:
        flash('Usuario não logado')
        return redirect(url_for('login'))


#Rota para logout
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


# Rotas para Cadastro de Fornecedor
@app.route('/cadastraFornecedor')
def cadastraFornecedor():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('cadastraFornecedor')))
    form = FormFornecedores(request.form)
    return render_template('cadastraFornecedor.html', titulo='CadastraFornecedor', form=form)


# Rota para criar o fornecedor
@app.route('/criarFornecedor', methods=['POST', ])
def criarFornecedor():
    form = FormFornecedores(request.form)

    if not form.validate_on_submit():
        return redirect(url_for('cadastraFornecedor'))

    cnpj = form.cnpj.data
    nome = form.nome.data
    cep = form.cep.data
    cidade = form.cidade.data
    estado = form.estado.data
    rua = form.rua.data
    numero = form.numero.data
    telefone = form.telefone.data
    email = form.email.data

    fornecedor = Fornecedores.query.filter_by(nome=nome).first()

    if fornecedor:
        flash('Fornecedor já cadastrado!')
        return redirect(url_for('listaFornecedor'))

    novo_fornecedor = Fornecedores(cnpj=cnpj, nome=nome, cep=cep, cidade=cidade, estado=estado, rua=rua, numero=numero,
                                   telefone=telefone, email=email)
    db.session.add(novo_fornecedor)
    db.session.commit()
    return redirect(url_for('listaFornecedor'))


# Rota para editar Fornecedor
@app.route('/editarFornecedor/<int:id_fornecedor>')
def editarFornecedor(id_fornecedor):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login',proxima=url_for('editarFornecedor')))
    fornecedor = Fornecedores.query.filter_by(id_fornecedor=id_fornecedor).first()
    form = FormFornecedores()
    form.cnpj.data = fornecedor.cnpj
    form.nome.data = fornecedor.nome
    form.cep.data= fornecedor.cep
    form.cidade.data = fornecedor.cidade
    form.estado.data = fornecedor.estado
    form.rua.data = fornecedor.rua
    form.numero.data = fornecedor.numero
    form.telefone.data = fornecedor.telefone
    form.email.data = fornecedor.email
    return render_template("editarFornecedor.html", fornecedor=fornecedor, titulo='Editar Fornecedor', form=form, id_fornecedor=id_fornecedor)


#Rota para atualizar Fornecedor
@app.route('/atualizarFornecedor', methods=['POST',])
def atualizarFornecedor():
    form = FormFornecedores(request.form)

    if form.validate_on_submit():
        fornecedor = Fornecedores.query.filter_by(id_fornecedor=request.form['id_fornecedor']).first()
        fornecedor.cnpj = form.cnpj.data
        fornecedor.nome = form.nome.data
        fornecedor.cep = form.cep.data
        fornecedor.cidade = form.cidade.data
        fornecedor.estado = form.estado.data
        fornecedor.rua = form.rua.data
        fornecedor.numero = form.numero.data
        fornecedor.telefone = form.telefone.data
        fornecedor.email = form.email.data

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

#Rota para listar clientes
@app.route('/listaCliente')
def listaCliente():
    lista_cliente = Clientes.query.order_by(Clientes.id_cliente)
    return render_template('listaCliente.html', titulo='Lista de Clientes', clientes=lista_cliente)

#Rota para cadastrar Cliente
@app.route('/cadastraCliente')
def cadastraCliente():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('cadastraCliente')))
    form = FormClientes(request.form)
    return render_template('cadastraCliente.html', titulo='Cadastrar Cliente', form=form)


# Rota para criar Cliente
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


# Rota para editar Cliente
@app.route('/editarCliente/<int:id_cliente>')
def editarCliente(id_cliente):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('editarCliente')))
    cliente = Clientes.query.filter_by(id_cliente=id_cliente).first()
    form = FormClientes()
    form.nome.data = cliente.nome
    form.documento.data = cliente.documento
    form.cep.data = cliente.cep
    form.cidade.data = cliente.cidade
    form.estado.data = cliente.estado
    form.rua.data = cliente.rua
    form.numero.data = cliente.numero
    form.telefone.data = cliente.telefone
    form.email.data = cliente.email

    return render_template("editarCliente.html", form=form, titulo='Editar Cliente', id_cliente=cliente.id_cliente)


#Rota para Atualizar Cliente
@app.route('/atualizarCliente', methods=['POST',])
def atualizarCliente():
    form = FormClientes(request.form)

    if form.validate_on_submit():
        cliente_id = request.form['id_cliente']
        cliente = Clientes.query.get(cliente_id)
        print(cliente_id)
        if cliente:
            try:
                form.populate_obj(cliente)
                db.session.add(cliente)  # Adicione esta linha para informar à sessão sobre as alterações
                db.session.commit()
                flash('Cliente atualizado com sucesso!', 'success')
            except Exception as e:
                flash(f'Erro ao atualizar o cliente: {str(e)}', 'danger')
                db.session.rollback()  # Desfaz as alterações em caso de erro
        else:
            flash('Cliente não encontrado.', 'danger')

    return redirect(url_for('listaCliente'))



# Rota Excluir Cliente
@app.route('/excluirCliente/<int:id_cliente>')
def excluirCliente(id_cliente):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))

    Clientes.query.filter_by(id_cliente=id_cliente).delete()
    db.session.commit()
    flash('Cliente exluido com sucesso!')
    return redirect(url_for('listaCliente'))


# Lista Matéria Prima
@app.route('/listaMateriaPrima')
def listaMateriaPrima():
    lista_material = MateriaPrima.query.order_by(MateriaPrima.id_materiaprima)
    return render_template('listaMateriaPrima.html', titulo='Lista de Material', materiais=lista_material)

@app.route('/cadastraMateriaPrima')
def cadastraMateriaPrima():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('cadastraMateriaPrima')))
    form = FormCadastraMateriaPrima(request.form)
    return render_template('cadastraMateriaPrima.html', titulo='Cadastrar Material', form=form)

# Rota para criar Materia Prima
@app.route('/criarMateriaPrima', methods=['POST', ])
def criarMateriaPrima():
    referencia_material = request.form['referencia_material']
    nome_material = request.form['nome_material']
    material = MateriaPrima.query.filter_by(referencia_material=referencia_material).first()

    if material:
        flash('Materia Prima ja cadastrada')
        return redirect(url_for('listaMateriaPrima'))

    novo_material = MateriaPrima(referencia_material=referencia_material, nome_material=nome_material)
    db.session.add(novo_material)
    db.session.commit()

    return redirect(url_for('listaMateriaPrima'))


# Rota para editar Materia Prima
@app.route('/editarMateriaPrima/<int:id_materiaprima>')
def editarMateriaPrima(id_materiaprima):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login',
                                proxima=url_for('editarMateriaPrima',
                                                         id_materiaprima=id_materiaprima)))
    material = MateriaPrima.query.filter_by(id_materiaprima=id_materiaprima).first()
    form = FormCadastraMateriaPrima()
    form.referencia_material.data = material.referencia_material
    form.nome_material.data = material.nome_material
    return render_template("editarMateriaPrima.html", form=form,
                           titulo='Editar Materia Prima',
                           id_materiaprima=material.id_materiaprima)


#Rota para Atualizar Materia Prima
@app.route('/atualizarMateriaPrima', methods=['POST',])
def atualizarMateriaPrima():
    form = FormCadastraMateriaPrima(request.form)

    if form.validate_on_submit():
        material = MateriaPrima.query.filter_by(id_materiaprima=request.form['id_materiaprima']).first()
        material.referencia_material = form.referencia_material.data
        material.nome_material = form.nome_material.data

        db.session.add(material)
        db.session.commit()

    return redirect(url_for('listaMateriaPrima'))


#Excluir Materia Prima
@app.route('/excluirMateriaPrima/<int:id_materiaprima>')
def excluirMateriaPrima(id_materiaprima):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))

    MateriaPrima.query.filter_by(id_materiaprima=id_materiaprima).delete()
    db.session.commit()
    flash('Materia Prima excluida com sucesso!')
    return redirect(url_for('listaMateriaPrima'))



#Lista Estoque Materia Prima
@app.route('/listaEstoqueMateriaPrima')
def listaEstoqueMateriaPrima():
    materiais = db.session.query(MateriaPrima, EstoqueMateriaPrima).join(EstoqueMateriaPrima, MateriaPrima.id_materiaprima == EstoqueMateriaPrima.materiaprima).all()

    return render_template('listaEstoqueM.html', titulo='Estoque Materia Prima', materiais=materiais)

@app.route('/cadastraEstoqueMateriaPrima')
def cadastraEstoqueMateriaPrima():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('cadastraEstoqueMateriaPrima')))
    form = EstoqueMateriaPrimaForm(request.form)
    form.materia_prima.choices = [(m.id_materiaprima, m.nome_material) for m in MateriaPrima.query.all()]
    return render_template('cadastraEstoqueMateriaPrima.html', titulo='Cadastro de Estoque Materia Prima', form=form)


@app.route('/criarEstoqueMateriaPrima', methods=['GET','POST', ])
def criarEstoqueMateriaPrima():
    form = EstoqueMateriaPrimaForm()
    if form.validate_on_submit():
        # Acesse os dados do formulário
        materia_prima_id = form.materia_prima.data
        quantidade = form.quantidade.data
        data_entrada = form.data_entrada.data
        data_validade = form.data_validade.data

        estoque_materia_prima = EstoqueMateriaPrima(
            materiaprima=materia_prima_id,
            quantidade=quantidade,
            data_entrada=data_entrada,
            data_validade=data_validade
        )
        db.session.add(estoque_materia_prima)
        db.session.commit()

    return redirect(url_for('listaEstoqueMateriaPrima'))



# Rota para editar Estoque de Materia Prima
@app.route('/editarEstoqueMateriaPrima/<int:id_estoque>')
def editarEstoqueMateriaPrima(id_estoque):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login',
                                proxima=url_for('editarEstoqueMateriaPrima',
                                                         id_estoque=id_estoque)))
    estoque = EstoqueMateriaPrima.query.filter_by(id_estoque=id_estoque).first()
    form = EstoqueMateriaPrimaForm()
    form.materia_prima.data = estoque.materiaprima
    form.quantidade.data = estoque.quantidade
    form.data_entrada.data = datetime.strptime(estoque.data_entrada, '%Y-%m-%d')
    form.data_validade.data = datetime.strptime(estoque.data_validade, '%Y-%m-%d')


    return render_template("editarEstoqueM.html", form=form,
                           titulo='Editar Materia Prima',
                           id_estoque=estoque.id_estoque)


@app.route('/atualizarEstoqueMateriaPrima', methods=['POST',])
def atualizarEstoqueMateriaPrima():
    form = EstoqueMateriaPrimaForm(request.form)

    if form.validate_on_submit():
        estoque = EstoqueMateriaPrima.query.filter_by(id_estoque=request.form['id_estoque']).first()
        estoque.materiaprima = form.materia_prima.data
        estoque.quantidade = form.quantidade.data
        estoque.data_entrada = form.data_entrada.data
        estoque.data_validade = form.data_validade.data
        db.session.add(estoque)
        db.session.commit()

    return redirect(url_for('listaEstoqueMateriaPrima'))

#Excluir Estoque
@app.route('/excluirEstoqueMateriaPrima/<int:id_estoque>')
def excluirEstoqueMateriaPrima(id_estoque):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))

    EstoqueMateriaPrima.query.filter_by(id_estoque=id_estoque).delete()
    db.session.commit()
    flash('Materia Prima excluida com sucesso!')
    return redirect(url_for('listaEstoqueMateriaPrima'))


#Rotas não implementada
'''
@app.route('/listaPedidos')
def listaPedidos():
    pedidos = db.session.query(Pedidos, Clientes, Item, Tamanho).join(Clientes).join(Item).join(Tamanho).all()
    print(pedidos)
    return render_template('listaPedidos.html', pedidos=pedidos)


# Rota para Registrar Pedido
@app.route('/registrarPedido')
def registrarPedido():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('registrarPedido')))
    form = FormRegistrarPedidos(request.form)
    return render_template('registrarPedido.html', titulo='Registrar Pedido', form=form)


# Rota para criar Pedido
@app.route('/criarPedido', methods=['POST', ])
def criarPedido():
    form = FormRegistrarPedidos(request.form)
    if not form.validate_on_submit():
        return redirect(url_for('registrarPedido'))

    select_cliente = form.select_cliente.data
    select_item = form.select_item.data
    select_tamanho = form.select_tamanho.data
    quantidade = form.quantidade.data

    pedido = Pedidos.query.filter_by(id_cliente=select_cliente).first()
    tamanho = Tamanho.query.filter_by(id_tamanho=select_tamanho).first()

    novo_pedido = Pedidos(id_cliente=select_cliente,
                          id_item=select_item,
                          sel_tamanho=select_tamanho,
                          quantidade=quantidade)
    db.session.add(novo_pedido)
    db.session.commit()
    return redirect(url_for('listaPedidos'))

'''



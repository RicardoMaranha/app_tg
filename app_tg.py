from flask import Flask, render_template, request

app = Flask(__name__)


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
    def __init__(self, cnpj, nome, endereco, telefone, email, id_fornecedor):
        self.cnpj = cnpj
        self.nome = nome
        self.endereco = endereco
        self.telefone = telefone
        self.email = email
        self.id_fornecedor = id_fornecedor


lista_fornecedor = []


@app.route('/inicio')
def inicio():
    fornecedor1 = Fornecedor('11111111001/0001', 'Fabrica de Borracha', 'Rua Amazonas', '16993933477', 'fb@gmail.com',
                             '1')
    fornecedor2 = Fornecedor('11111111001/0001', 'Fabrica de Borracha', 'Rua Amazonas', '16993933477', 'fb@gmail.com',
                             '1')
    lista_fornecedor = [fornecedor1, fornecedor2]
    siteNome = "Home"
    return render_template('index.html', fornecedores=lista_fornecedor)


@app.route('/teste')
def teste():
    fornecedor1 = Fornecedor('11111111001/0001', 'Fabrica de Borracha', 'Rua Amazonas', '16993933477', 'fb@gmail.com',
                             '1')
    fornecedor2 = Fornecedor('11111111001/0001', 'Fabrica de Borracha', 'Rua Amazonas', '16993933477', 'fb@gmail.com',
                             '1')
    lista_fornecedor = [fornecedor1, fornecedor2]
    return render_template('listaFornecedor.html', fornecedores=lista_fornecedor)


app.run(debug=True)

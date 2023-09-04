
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

class Pedido:
    def __init__(self, id_pedido, data_pedido):
        self.id_pedido = id_pedido
        self.data_pedido = data_pedido
        self.itens = []

class Iten:
    def __init__(self, id_iten, nome, preco):
        self.id_iten = id_iten
        self.nome = nome
        self.preco = preco


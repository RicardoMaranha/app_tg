from app_tg import db



class Usuarios(db.Model):
    nickname = db.Column(db.String(50), primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    senha = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<NAME %r>' % self.name


class Clientes(db.Model):
    id_cliente = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    documento = db.Column(db.String(18), unique=True, nullable=False)
    cep = db.Column(db.String(10))
    cidade = db.Column(db.String(100))
    estado = db.Column(db.String(50))
    rua = db.Column(db.String(255))
    numero = db.Column(db.String(20))
    telefone = db.Column(db.String(50))
    email = db.Column(db.String(50))


class Ficha(db.Model):
    id_ficha = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    documento = db.Column(db.String(18), unique=True, nullable=False)
    cep = db.Column(db.String(10))
    cidade = db.Column(db.String(100))
    estado = db.Column(db.String(50))
    rua = db.Column(db.String(255))
    numero = db.Column(db.String(20))
    telefone = db.Column(db.String(50))
    email = db.Column(db.String(50))


class MateriaPrima(db.Model):
    __tablename__ = 'materiaprima'
    id_materiaprima = db.Column(db.Integer, primary_key=True, autoincrement=True)
    referencia_material = db.Column(db.String(255), nullable=False)
    nome_material = db.Column(db.String(100), nullable=False)


class EstoqueMateriaPrima(db.Model):
    __tablename__ = 'estoquemateriaprima'
    id_estoque = db.Column(db.Integer, primary_key=True, autoincrement=True)
    materiaprima = db.Column(db.Integer, db.ForeignKey('materiaprima.id_materiaprima'))
    quantidade = db.Column(db.Integer)
    data_entrada = db.Column(db.String(10), nullable=False)
    data_validade= db.Column(db.String(10), nullable=False)

    # rl_materiaprima = db.relationship('MateriaPrima', backref='estoque_produto', primaryjoin='estoquemateriaprima.materiaprima == materiaprima.id_materiaprima')


class Fornecedores(db.Model):
    id_fornecedor = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    cnpj = db.Column(db.String(18), unique=True, nullable=False)
    cep = db.Column(db.String(10))
    cidade = db.Column(db.String(100))
    estado = db.Column(db.String(50))
    rua = db.Column(db.String(255))
    numero = db.Column(db.String(20))
    telefone = db.Column(db.String(50))
    email = db.Column(db.String(50))

# Modelos Não implementados
'''
class Item(db.Model):
    __tablename__ = 'item'
    id_item = db.Column(db.Integer, primary_key=True, autoincrement=True)
    referencia = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(255))
'''
'''
class Tamanho(db.Model):
    __tablename__ = 'tamanho'

    id_tamanho = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tamanho = db.Column(db.String(50), nullable=False)
'''
'''
class EstoqueProduto(db.Model):
    __tablename__ = 'estoqueproduto'
    id_item = db.Column(db.Integer, db.ForeignKey('Item.id_item'), primary_key=True)
    tamanho = db.Column(db.Integer, db.ForeignKey('Tamanho.id_tamanho'))
    quantidade = db.Column(db.Integer)
    # Outros campos relacionados ao estoque
    rl_item = db.relationship('Item', backref='estoque_produto', uselist=False, primaryjoin='estoqueproduto.id_item == item.id_item')
    rl_tamanho = db.relationship('Tamanho', backref='estoque_produto', uselist=False, primaryjoin='estoqueproduto.tamanho == tamanho.id_tamanho')
'''

'''
class ProdutoMateriaPrima(db.Model):
    __tablename__ = 'produtomateriaprima'
    id_item = db.Column(db.Integer, db.ForeignKey('item.id_item'), primary_key=True)
    id_materiaprima = db.Column(db.Integer, db.ForeignKey('materiaprima.id_materiaprima'), primary_key=True)
    quantidade_materiaprima = db.Column(db.Float, nullable=False)

    rl_item = db.relationship('Item', backref='estoque_produto', uselist=False, primaryjoin='produtomateriaprima.id_item == item.id_item')
    rl_materia_prima = db.relationship('MateriaPrima', backref='estoque_produto')

'''
'''
class Pedidos(db.Model):
    id_pedido = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_cliente = db.Column(db.Integer, db.ForeignKey('clientes.id_cliente'))
    id_item = db.Column(db.Integer, db.ForeignKey('item.id_item'))
    sel_tamanho = db.Column(db.Integer, db.ForeignKey('tamanho.id_tamanho'))
    quantidade = db.Column(db.Integer, nullable=False)
'''































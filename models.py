from app_tg import db

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

    def __repr__(self):
        return '<NAME %r>' % self.name


class Usuarios(db.Model):
    nickname = db.Column(db.String(50), primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    senha = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<NAME %r>' % self.name
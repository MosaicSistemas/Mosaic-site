from app import db
from flask_login import UserMixin

class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer(), nullable=False, primary_key=True)
    usuario = db.Column(db.String(30), nullable=False, unique=False)
    email = db.Column(db.String(30), nullable=False, unique=True)
    senha = db.Column(db.String(30), nullable=False)
    status = db.Column(db.String(5), nullable=False)

    def __init__(self, usuario, email, senha, status):
        self.usuario = usuario
        self.email = email
        self.senha = senha
        self.status = status

class Produto(db.Model):
    id = db.Column(db.String(13), nullable=False, primary_key=True)
    nome = db.Column(db.String(50) , nullable=False, unique=True)
    categoria = db.Column(db.String(30) , nullable=False)
    medida = db.Column(db.String(30) , nullable=False)
    custo = db.Column(db.Float(), nullable=False)
    valor = db.Column(db.Float(), nullable=False)

    def __init__(self, id, nome, categoria, medida, custo, valor):
        self.id = id
        self.nome = nome
        self.categoria = categoria
        self.medida = medida
        self.custo = custo
        self.valor = valor

if __name__ == '__main__':
    db.drop_all()
    db.create_all()
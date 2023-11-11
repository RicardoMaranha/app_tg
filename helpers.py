import os
from app_tg import app
from app_tg import db
from models import *
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, validators, SelectField, IntegerField


class FormUsuario(FlaskForm):
    nickname = StringField('Nome de Usuário',  [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={ "placeholder" : "User"})
    senha = PasswordField('Senha', [validators.DataRequired(), validators.Length(min=1, max=100)], render_kw={ "placeholder" : "Senha"})
    login = SubmitField('Login')


class FormFornecedores(FlaskForm):
    cnpj = StringField('CNPJ', [validators.DataRequired(), validators.Length(min=1, max=18)], render_kw={ "placeholder" : "12.345.678/0001-00"})
    nome = StringField('Nome', [validators.DataRequired(), validators.Length(min=1, max=18)], render_kw={"placeholder":"Amazonas S.A."})
    cep = StringField('CEP', [validators.DataRequired(), validators.Length(min=1,max=10)], render_kw={"placeholder":"14407-139"})
    cidade = StringField('Cidade', [validators.DataRequired(), validators.Length(min=1,max=100)], render_kw={"placeholder":"Franca"})
    estado= StringField('Estado', [validators.DataRequired(), validators.Length(min=1, max=50)],render_kw={"placeholder":"SP"})
    rua = StringField('Rua', [validators.DataRequired(), validators.Length(min=1, max=255)], render_kw={"placeholder":"Rua Industrial"})
    numero = StringField('Numero', [validators.DataRequired(), validators.Length(min=1, max=20)], render_kw={"placeholder":"3031"})
    telefone = StringField('Telefone', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={"placeholder":"16 99142-4555"})
    email = StringField('Email', [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={"placeholder":"amazonas@gmail.com"})
    salvar = SubmitField('Salvar')

class FormCadastraMateriaPrima(FlaskForm):
    referencia_material = StringField('Referencia',
                                      [validators.DataRequired(),
                                       validators.Length(min=1, max=255)],
                                      render_kw = {"placeholder": "bo00123"})
    nome_material = StringField('Nome',
                                [validators.DataRequired(),
                                 validators.Length(min=1, max=100)],
                                render_kw={"placeholder": "Borracha"})
    salvar = SubmitField('Registrar Matéria Prima')


class EstoqueMateriaPrima(FlaskForm):
    materiaprima = SelectField('Materia Prima',
                               coerce=int,
                               validators=[validators.DataRequired()])
    quantidade = IntegerField('Quantidade',
                              validators=[validators.DataRequired(),
                                          validators.NumberRange(min=0, max=1000)])
    salvar = SubmitField('Salvar')

    def __init__(self, *args, **kwargs):
        super(EstoqueMateriaPrima, self).__init__(*args, **kwargs)
        self.materiaprima.choices = [(material.id_materiaprima, MateriaPrima.nome_material) for material in MateriaPrima.query.all()]



class FormClientes(FlaskForm):
    documento = StringField('Documento', [validators.DataRequired(), validators.Length(min=1, max=18)])
    nome = StringField('Nome', [validators.DataRequired(), validators.Length(min=1, max=18)])
    cep = StringField('CEP', [validators.DataRequired(), validators.Length(min=1, max=10)])
    cidade = StringField('Cidade', [validators.DataRequired(), validators.Length(min=1, max=100)])
    estado = StringField('Estado', [validators.DataRequired(), validators.Length(min=1, max=50)])
    rua = StringField('Rua', [validators.DataRequired(), validators.Length(min=1, max=255)])
    numero = StringField('Numero', [validators.DataRequired(), validators.Length(min=1, max=20)])
    telefone = StringField('Telefone', [validators.DataRequired(), validators.Length(min=1, max=50)])
    email = StringField('Email', [validators.DataRequired(), validators.Length(min=1, max=50)])
    salvar = SubmitField('Salvar')


# class FormRegistrarMaterial(FlaskForm):
class FormRegistrarPedidos(FlaskForm):
    select_cliente = SelectField('Cliente', coerce=int, validators=[validators.DataRequired()])
    select_item = SelectField('Item', coerce=int, validators=[validators.DataRequired()])
    quantidade = IntegerField('Quantidade',
                              validators=[validators.DataRequired(), validators.NumberRange(min=0, max=1000)])
    select_tamanho = SelectField('Tamanho', coerce=int, validators=[validators.DataRequired()])
    salvar = SubmitField('Salvar Pedido')

    def __init__(self, *args, **kwargs):
        super(FormRegistrarPedidos, self).__init__(*args, **kwargs)
        self.select_cliente.choices = [(cliente.id_cliente, cliente.nome) for cliente in Clientes.query.all()]
        self.select_item.choices = [(item.id_item, item.referencia) for item in Item.query.all()]
        self.select_tamanho.choices = [(tamanho.id_tamanho, tamanho.tamanho_item) for tamanho in Tamanho.query.all()]



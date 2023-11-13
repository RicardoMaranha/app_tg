import os
from app_tg import app
from app_tg import db
from models import *
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, validators, SelectField, IntegerField, DateField, HiddenField
from wtforms.validators import DataRequired, NumberRange

class FormUsuario(FlaskForm):
    nickname = StringField('Nome de Usuário',  [validators.DataRequired(), validators.Length(min=1, max=50)], render_kw={ "placeholder" : "User"})
    senha = PasswordField('Senha', [validators.DataRequired(), validators.Length(min=1, max=100)], render_kw={ "placeholder" : "Senha"})
    login = SubmitField('Login')
    logout = SubmitField('Logout')


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
    referencia_material= StringField('Referência Materia Prima',
                                       [validators.DataRequired(),
                                       validators.Length(min=1, max=255)],
                                      render_kw = {"placeholder": "bo00123"})
    nome_material = StringField('Nome Materia Prima',
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
    nome = StringField('Nome', [validators.DataRequired(), validators.Length(min=1, max=18)])
    documento = StringField('Documento', [validators.DataRequired(), validators.Length(min=1, max=18)])
    cep = StringField('CEP', [validators.DataRequired(), validators.Length(min=1, max=10)])
    cidade = StringField('Cidade', [validators.DataRequired(), validators.Length(min=1, max=100)])
    estado = StringField('Estado', [validators.DataRequired(), validators.Length(min=1, max=50)])
    rua = StringField('Rua', [validators.DataRequired(), validators.Length(min=1, max=255)])
    numero = StringField('Numero', [validators.DataRequired(), validators.Length(min=1, max=20)])
    telefone = StringField('Telefone', [validators.DataRequired(), validators.Length(min=1, max=50)])
    email = StringField('Email', [validators.DataRequired(), validators.Length(min=1, max=50)])
    salvar = SubmitField('Salvar')


class EstoqueMateriaPrimaForm(FlaskForm):
    tipos = ['placa','gr','kg', 'lt', 'ml']
    materia_prima = SelectField('Matéria Prima', coerce=int, validators=[DataRequired()])
    quantidade = IntegerField('Quantidade', validators=[DataRequired()])
    tipo = SelectField('Tipo', choices=tipos)
    data_entrada = DateField('Data de Entrada (YYYY-MM-DD)', validators=[DataRequired()])
    data_validade = DateField('Data de Validade (YYYY-MM-DD)', validators=[DataRequired()])
    salvar = SubmitField('Salvar')

    def __init__(self, *args, **kwargs):
        super(EstoqueMateriaPrimaForm, self).__init__(*args, **kwargs)

        # Popule as opções do campo materia_prima
        self.materia_prima.choices = [(mp.id_materiaprima, mp.nome_material) for mp in MateriaPrima.query.all()]


class solicitarEstoqueMateriaPrimaForm(FlaskForm):
    id_estoque = HiddenField('ID Estoque', validators=[DataRequired()])
    quantidade = IntegerField('Quantidade a Retirar', validators=[DataRequired(), NumberRange(min=1)])
    retirar = SubmitField('Retirar')


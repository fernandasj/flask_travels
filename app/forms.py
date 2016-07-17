# coding=utf-8

from flask.ext.wtf import Form
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired


class VeiculoForm(Form):
    Id_veiculo = StringField('Id_veiculo')
    Placa = StringField('Placa')
    Modelo = StringField('Modelo')
    Status = StringField('Status')

class MotoristaForm(Form):
    Id_motorista = StringField('Id_motorista')
    Matricula = StringField('Matricula')
    Nome = StringField('Nome')
    CNH = StringField('CNH')
    Status = StringField('Status')

class ViagemForm(Form):
    Id_viagem = StringField('Id_viagem')
    Cod_veiculo = StringField('Cod_veiculo')
    Cod_motorista = StringField('Cod_motorista')
    DATA_SAIDA = StringField('DATA_SAIDA')
    DATA_CHEGADA = StringField('DATA_CHEGADA')
    KM_SAIDA = IntegerField('KM_SAIDA')
    KM_CHEGADA = IntegerField('KM_CHEGADA')
    Solicitante = StringField('Solicitante')
    Descricao = StringField('Descricao')
    Status = StringField('Status')

class RevisaoForm(Form):
    Id_revisao = StringField('Id_revisao')
    Cod_veiculo = StringField('Cod_veiculo')
    Descricao = StringField('Descricao')
    DATA_REVISAO = StringField('DATA_REVISAO')
    Status = StringField('Status')

class UsuarioForm(Form):
    Id_usuario = StringField('Id_usuario')
    Matricula = StringField('Matricula')
    Nome = StringField('Nome')
    CPF = StringField('CPF')
    Email = StringField('Email')
    Senha = StringField('Senha')

class LoginForm(Form):
    Matricula = StringField('Matricula')
    Senha = StringField('Senha')

class FinalizarForm(Form):
    DATA_CHEGADA = StringField('DATA_CHGADA')
    KM_CHEGADA = StringField('KM_CHEGADA')

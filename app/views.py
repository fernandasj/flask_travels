# -*- coding: utf-8 -*-

from app import app
from forms import *

import psycopg2
import psycopg2.extras

from flask import render_template, request, redirect, url_for

try:
    conn = psycopg2.connect(dbname="transporte", host="localhost", user="postgres", password="123456")
    print "conectado"
except:
    print "falha ao conectar com o banco"


@app.route('/', methods=['POST', 'GET'])
@app.route('/login', methods=['POST', 'GET'])
def login():


    form = LoginForm()

    #POST
    if request.method == 'POST':
        Matricula = request.form['Matricula']
        Senha = request.form['Senha']

        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cur.execute("SELECT * FROM usuario U WHERE '%s'=U.matricula and '%s'=U.senha"%(Matricula, Senha))

        usuarios = cur.fetchone()

        if usuarios:
            return render_template('index.html', title="IFPB Transportes")
        else:
            return render_template('usuario/login.html', title="Login", form=form, result="Senha ou usuario invalidos")

    # GET

    return render_template('usuario/login.html', title="Login", form=form)

@app.route('/ifpb_transportes')
def menu():
    return render_template('index.html', title='IFPB Transportes')

# usuario

@app.route('/add_usuario', methods=['GET', 'POST'])
def add_usuario():

    form = UsuarioForm()

    # POST

    if request.method == 'POST':
        Matricula = request.form['Matricula']
        Nome = request.form['Nome']
        CPF = request.form['CPF']
        Email = request.form['Email']
        Senha = request.form['Senha']

        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("INSERT INTO usuario (matricula, nome, cpf, email, senha) VALUES ('%s', '%s', '%s', '%s', '%s')"%(Matricula, Nome, CPF, Email, Senha))

        conn.commit()

        return render_template('usuario/create_usuario.html', title="Criar Conta", form=form)

    #GET
    return render_template('usuario/create_usuario.html', title="Criar Conta", form=form)

@app.route('/editar_usuario/<id_usuario>', methods=['GET', 'POST'])
def update_usuario(id_usuario=None):
    form = UsuarioForm()

    #POST
    if request.method == 'POST':
        Matricula = request.form['Matricula']
        Nome = request.form['Nome']
        CPF = request.form['CPF']
        Email = request.form['Email']
        Senha = request.form['Senha']

        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("UPDATE usuario SET matricula = '%s', nome = '%s',  cpf = '%s', email = '%s', senha = '%s' WHERE id_usuario = '%s'"%(Matricula, Nome, CPF, Email, Senha, id_usuario))
        conn.commit()

        return redirect(url_for('list_usuario'))


    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("""SELECT * FROM usuario WHERE Id_usuario = '%s'""" % id_usuario)
    usuario = cur.fetchone()
    return render_template('usuario/update_usuario.html', usuario=usuario, form=form, title='Editar Usuario')

@app.route('/list_usuario')
def list_usuario():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("""SELECT * FROM Usuario""")
    usuarios = cur.fetchall()

    return render_template('usuario/list_usuario.html', title="Lista de Usuarios", usuarios=usuarios)

@app.route('/del_usuario/<id_usuario>', methods=['GET'])
def delete(id_usuario):

    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("""DELETE FROM usuario WHERE Id_usuario = '%s'""" % id_usuario)
    conn.commit()

    return redirect(url_for('list_usuario'))


#veiculo
@app.route('/veiculo')
def veiculo():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("""SELECT * FROM Veiculo WHERE status != 'Removido'""")
    veiculos = cur.fetchall()

    return render_template('veiculo/list_veiculo.html', title="Lista de Veiculos", veiculos=veiculos)


@app.route('/add_veiculo', methods=['GET', 'POST'])
def add_veiculo():

    form = VeiculoForm()

    #POST
    if request.method == 'POST':
        Placa = request.form['Placa']
        Modelo = request.form['Modelo']

        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("INSERT INTO veiculo (placa, modelo, status) VALUES ('%s', '%s', 'Livre')"%(Placa, Modelo))

        conn.commit()

        return render_template('veiculo/create_veiculo.html', title="Adicionar Veiculo", form=form)

    #GET
    return render_template('veiculo/create_veiculo.html', title="Adicionar Veiculo", form=form)


@app.route('/editar_veiculo/<id_veiculo>', methods=['GET', 'POST'])
def editar_veiculo(id_veiculo=None):
    form = VeiculoForm()

    if request.method == 'POST':
        Placa = request.form['Placa']
        Modelo = request.form['Modelo']

        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("UPDATE veiculo SET placa = '%s', modelo = '%s' WHERE id_veiculo = '%s'"%(Placa, Modelo, id_veiculo))

        conn.commit()

        return redirect(url_for('veiculo'))

    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("""SELECT * FROM veiculo WHERE Id_veiculo = '%s'"""% id_veiculo)
    veiculo = cur.fetchone()
    return render_template('veiculo/update_veiculo.html', veiculo=veiculo, form=form, title='Editar Veiculo')


@app.route('/del_veiculo/<id_veiculo>', methods = ['GET'])
def delete_veiculo(id_veiculo):

    if request.method == 'GET':
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("""UPDATE veiculo SET status='Removido' WHERE Id_veiculo = '%s'""" % id_veiculo)
        conn.commit()

        return redirect(url_for('veiculo'))


#motorista
@app.route('/motorista')
def motorista():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("""SELECT * FROM motorista WHERE status is null""")
    motoristas = cur.fetchall()

    return render_template('motorista/list_motorista.html', title="Lista de Motoristas", motoristas=motoristas)

@app.route('/add_motorista', methods=['GET', 'POST'])
def add_motorista():

    form = MotoristaForm()

    #POST
    if request.method == 'POST':
        Matricula = request.form['Matricula']
        Nome = request.form['Nome']
        CNH = request.form['CNH']


        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("INSERT INTO motorista (matricula, nome, cnh) VALUES ('%s', '%s', '%s')"%(
            Matricula, Nome, CNH))

        conn.commit()

        return redirect(url_for('motorista'))
        # return render_template('motorista/create_motorista.html', title="Adicionar Motorista", form=form)

    #GET
    return render_template('motorista/create_motorista.html', title="Adicionar Motorista", form=form)


@app.route('/editar_motorista/<id_motorista>', methods=['GET', 'POST'])

def editar_motorista(id_motorista=None):
    form = MotoristaForm()

    #POST
    if request.method == 'POST':
        Matricula = request.form['Matricula']
        Nome = request.form['Nome']
        CNH = request.form['CNH']

        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("UPDATE motorista SET matricula = '%s', nome = '%s',  cnh = '%s' WHERE id_motorista = '%s'"%(Matricula, Nome, CNH, id_motorista))

        conn.commit()

        return redirect(url_for('motorista'))


    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("""SELECT * FROM motorista WHERE Id_motorista = '%s'""" % id_motorista)
    motorista = cur.fetchone()
    return render_template('motorista/update_motorista.html', motorista=motorista, form=form, title='Editar Motorista')

@app.route('/del_motorista/<id_motorista>', methods=['GET'])
def del_motorista(id_motorista):

    if request.method == 'GET':
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("""UPDATE motorista SET status = 'Removido' WHERE Id_motorista = '%s'""" % id_motorista)
        conn.commit()
        return redirect(url_for('motorista'))


#viagem
@app.route('/viagem')
def viagem():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("""SELECT * FROM viagem WHERE status is null""")
    viagens = cur.fetchall()
    return render_template('viagem/list_viagem.html', title="Lista de Viagens", viagens=viagens)


@app.route('/add_viagem', methods=['GET', 'POST'])
def add_viagem():

    form = ViagemForm()

    #POST
    if request.method == 'POST':
        Cod_veiculo = request.form['Cod_veiculo']
        Cod_motorista = request.form['Cod_motorista']
        DATA_SAIDA = request.form['DATA_SAIDA']
        KM_SAIDA = request.form['KM_SAIDA']
        Solicitante = request.form['Solicitante']
        Descricao = request.form['Descricao']

        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("INSERT INTO viagem (cod_veiculo, cod_motorista, data_saida, km_saida, solicitante, descricao) VALUES  ( '%s', '%s', '%s','%s', '%s', '%s')"%
            (Cod_veiculo, Cod_motorista, DATA_SAIDA, KM_SAIDA, Solicitante, Descricao))

        cur.execute("UPDATE veiculo SET status = 'Viajando' WHERE id_veiculo = '%s'"% Cod_veiculo)

        conn.commit()

        return render_template('viagem/create_viagem.html', title="Adicionar Viagem", form=form)

    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("""SELECT * FROM motorista WHERE status is null""")
    motoristas = cur.fetchall()

    # cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("""SELECT * FROM veiculo""")
    veiculos = cur.fetchall()

    return render_template('viagem/create_viagem.html', title="Adicionar Viagem", form=form, motoristas=motoristas,veiculos=veiculos)

@app.route('/editar_viagem/<id_viagem>', methods=['GET', 'POST'])
def editar_viagem(id_viagem=None):

    form = ViagemForm()

    #POST
    if request.method == 'POST':
        Cod_veiculo = request.form['Cod_veiculo']
        Cod_motorista = request.form['Cod_motorista']
        DATA_SAIDA = request.form['DATA_SAIDA']
        DATA_CHEGADA = request.form['DATA_CHEGADA']
        KM_SAIDA = request.form['KM_SAIDA']
        KM_CHEGADA = request.form['KM_CHEGADA']
        Solicitante = request.form['Solicitante']
        Descricao = request.form['Descricao']

        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("UPDATE viagem SET cod_veiculo = '%s', cod_motorista = '%s',  data_saida = '%s', data_chegada = '%s', km_saida = '%s', km_chegada = '%s', solicitante = '%s', descricao = '%s' WHERE id_viagem = '%s'"%(Cod_veiculo, Cod_motorista, DATA_SAIDA, DATA_CHEGADA, KM_SAIDA, KM_CHEGADA, Solicitante, Descricao, id_viagem))

        conn.commit()

        return redirect(url_for('viagem'))


    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("""SELECT * FROM viagem WHERE Id_viagem = '%s'""" % id_viagem)
    viagem = cur.fetchone()
    return render_template('viagem/update_viagem.html', viagem=viagem, form=form, title='Editar Viagem')


@app.route('/del_viagem/<id_viagem>', methods=['GET'])
def delete_viagem(id_viagem):
    if request.method == 'GET':
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("""UPDATE viagem SET status = 'Removido' WHERE Id_viagem = '%s'""" % id_viagem)
        conn.commit()

        return redirect(url_for('viagem'))

@app.route('/finalizar_viagem/<id_viagem>', methods=['GET', 'POST'])
def finalizar_viagem(id_viagem):
    form = FinalizarForm()

    if request.method == 'POST':
        DATA_CHEGADA = request.form['DATA_CHEGADA']
        KM_CHEGADA = request.form['KM_CHEGADA']

        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("UPDATE viagem SET data_chegada = '%s', km_chegada = '%s' WHERE id_viagem= '%s'"%(DATA_CHEGADA, KM_CHEGADA, id_viagem))

        cur.execute("SELECT * FROM viagem WHERE id_viagem = '%s'"%id_viagem)
        veiculo = cur.fetchone()

        cur.execute("SELECT * FROM viagem WHERE id_viagem = '%s'"%id_viagem)
        viagem = cur.fetchone()

        if (int(KM_CHEGADA) - int(viagem['km_saida']) >= 1000):
            cur.execute("UPDATE veiculo SET status = 'Revisao' WHERE id_veiculo = '%s'"%veiculo['cod_veiculo'])
        else:
            cur.execute("UPDATE veiculo SET status = 'Livre' WHERE id_veiculo = '%s'"%veiculo['cod_veiculo'])

        conn.commit()

        return redirect(url_for('viagem'))

    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("""SELECT * FROM viagem WHERE Id_viagem = '%s'""" % id_viagem)
    viagem = cur.fetchone()
    return render_template('viagem/finalizar_viagem.html', viagem=viagem, form=form, title='Finalizar Viagem')

#revisao
@app.route('/revisao')
def revisao():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("""SELECT * FROM Revisao WHERE status is null""")
    revisoes = cur.fetchall()

    return render_template('revisao/list_revisao.html', title="Lista de Revisoes", revisoes=revisoes)


@app.route('/add_revisao', methods=['GET', 'POST'])
def add_revisao():
    form = RevisaoForm()

    #POST
    if request.method == 'POST':
        Cod_veiculo = request.form['Cod_veiculo']
        Descricao = request.form['Descricao']
        DATA_REVISAO = request.form['DATA_REVISAO']


        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("INSERT INTO revisao (cod_veiculo, descricao, data_revisao) VALUES ('%s', '%s', '%s')"%(Cod_veiculo, Descricao, DATA_REVISAO))

        cur.execute("UPDATE veiculo SET status = 'Revisado' WHERE id_veiculo = '%s'"%Cod_veiculo)

        conn.commit()

        return render_template('revisao/create_revisao.html', title="Adicionar Revisao", form=form)

    #GET
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("""SELECT * FROM veiculo""")
    veiculos = cur.fetchall()
    return render_template('revisao/create_revisao.html', title="Adicionar Revisao", form=form, veiculos=veiculos)

@app.route('/editar_revisao/<id_revisao>', methods=['GET', 'POST'])
def editar_revisao(id_revisao=None):
    form = RevisaoForm()

    #POST
    if request.method == 'POST':
        Cod_veiculo = request.form['Cod_veiculo']
        Descricao = request.form['Descricao']
        DATA_REVISAO = request.form['DATA_REVISAO']

        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("UPDATE revisao SET cod_veiculo = '%s',  descricao = '%s', data_revisao = '%s' WHERE id_revisao = '%s'"%(Cod_veiculo, Descricao, DATA_REVISAO, id_revisao))

        conn.commit()

        return redirect(url_for('revisao'))

    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("""SELECT * FROM revisao WHERE Id_revisao = '%s'""" % id_revisao)
    revisao = cur.fetchone()
    return render_template('revisao/update_revisao.html', revisao=revisao, form=form, title='Editar Revisao')


@app.route('/del_revisao/<id_revisao>', methods=['GET'])
def delete_revisao(id_revisao):
    if request.method == 'GET':
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("""UPDATE revisao SET status = 'Removido' WHERE Id_revisao = '%s'""" % id_revisao)
        conn.commit()

        return redirect(url_for('revisao'))

if __name__ == '__main__':
    app.debug = True
    app.run()

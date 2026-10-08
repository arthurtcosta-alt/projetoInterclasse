from flask import Flask, render_template, request, redirect, url_for, flash, g
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from banco import tabela_time, tabela_partida, tabela_jogador
from database import *

app = Flask(__name__)
app.secret_key = "chave-secreta-interclasse-2026"


@app.route("/")
def dashboard():
    times = tabela_time.select_quantidade_total()
    jogadores = tabela_jogador.select_quantidade_total()
    partidas = tabela_partida.select_quantidade_total()
    return render_template(
        "dashboard.html",
        total_jogadores=jogadores,
        total_times=times,
        total_partidas= partidas,
        proximas_partidas=0,
        times_ranking=0,
    )


@app.route("/jogadores")
def listar_jogadores():
    jogadores = tabela_jogador.select_todos_jogadores()
    return render_template("jogadores.html", jogadores=jogadores)
@app.route("/jogadores/novo", methods=["GET", "POST"])
def novo_jogador():
    if request.method == "POST":
        # 1- pegar os valores do form
        nome = request.form.get("nome", "").strip()
        numero_camisa = request.form.get("numero_camisa", "").strip()
        posicao = request.form.get("posicao", "").strip()
        time_id = request.form.get("time_id", "").strip()
        # 2- verificar c foi digitalizado
        if not nome:
            flash('Digite o nome do jogador', 'error')
            return redirect(url_for(novo_jogador))
        if not numero_camisa:
            flash('Digite numero do jogador', 'error')
            return redirect(url_for(novo_jogador))
        if not posicao:
            flash('Digite a posição do jogador ', 'error')
            return redirect(url_for(novo_jogador))
        if not time_id:
            flash('Digite o time do jogador ', 'error')
            return redirect(url_for(novo_jogador))
    jogadores = tabela_jogador.select_todos_jogadores()
    times = tabela_time.select_todos_times()
    return render_template("jogadores.html", times=times, jogadores=jogadores)
@app.route("/times")
def listar_times():
    times = tabela_time.select_todos_times()
    return render_template("times.html", times=times)


@app.route("/times/novo", methods=["GET", "POST"])
def novo_time():

    if request.method == "POST":
        # 1- pegar os valores do form
        nome = request.form.get("nome", "").strip()
        turma = request.form.get("turma", "").strip()
        responsavel = request.form.get("responsavel", "").strip()
        # 2- verificar c foi digitalizado
        if not nome:
            flash('Digite o nome do time', 'error')
            return redirect(url_for(novo_time))
        if not turma:
            flash('Digite a turma', 'error')
            return redirect(url_for(novo_time))
        if not responsavel:
            flash('Digite o responsável', 'error')
            return redirect(url_for(novo_time))
        # 3- salvar no banco
        tabela_time.salvar(nome=nome, turma=turma, responsavel=responsavel)
    times = tabela_time.select_todos_times()
    print(times)
    return render_template("times.html", times=times)



@app.route("/partidas")
def listar_partidas():
    partidas = tabela_partida.select_todas_partidas()  # agora sim é a lista
    print(partidas)
    return render_template("partidas.html", partidas=partidas)


@app.route("/partidas/nova", methods=["GET", "POST"])
def nova_partida():

    if request.method == "POST":
        time_casa_id = request.form.get("time_casa_id")
        time_visitante_id = request.form.get("time_visitante_id")
        gols_casa = request.form.get("gols_casa") or 0
        gols_visitante = request.form.get("gols_visitante") or 0
        data_partida = request.form.get("data_partida", "").strip()
        if not time_casa_id:
            flash('Digite o time da casa ', 'error')
            return render_template("partidas.html")
        if not time_visitante_id:
            flash('Digite o time visitante', 'error')
            return redirect(url_for(nova_partida))
        if not gols_casa:
            flash('Digite o total de gols do time da casa', 'error')
            return redirect(url_for(nova_partida))
        if not gols_visitante:
            flash('Digite o total de gols do time visitante', 'error')
            return redirect(url_for(nova_partida))
        if not data_partida:
            flash('Digite a data da partida', 'error')
            return redirect(url_for(nova_partida))
        if time_casa_id == time_visitante_id:
            flash("Selecione times diferentes", "error")
            return redirect(url_for(nova_partida))

        # 3
        tabela_partida.salvar(time_casa_id=time_casa_id, time_visitante_id=time_visitante_id, gols_casa=gols_casa, gols_visitante=gols_visitante, data_partida=data_partida)
    times = tabela_time.select_todos_times()
    partidas = tabela_partida.select_todas_partidas()


    return render_template("partidas.html", partidas=partidas, times=times)


if __name__ == "__main__":
    app.run(debug=True)

from flask import flash
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from database import Partida, db_session, Jogador


def select_todos_jogadores():
    # buscar todos os times no banco
    # 1- montar o SELECT
    jogadores_sql = select(Jogador)  # não é a lista de times ainda
    # 2- executar o SELECT
    jogadores = db_session.execute(jogadores_sql).scalars().all()  # agora sim é a lista
def salvar(nome, numero_camisa, posicao, time_id):
    try:
        jogador_novo = Jogador(nome=nome, numero_camisa=int(numero_camisa), posicao=posicao, time_id=time_id)
        db_session.add(jogador_novo)
        db_session.commit()
        flash('jogador cadastrado com sucesso', 'success')
    except SQLAlchemyError as e:
        db_session.rollback()
        flash('ocorreu um erro, tente novamente', 'error')
        print(f"Erro: {e}")
    except Exception as e:
        db_session.rollback()
        flash('ocorreu um erro, tente novamente', 'error')
        print(f"Erro: {e}")
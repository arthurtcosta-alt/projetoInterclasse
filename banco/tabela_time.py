from flask import flash
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from database import Time, db_session, Jogador


def select_todos_times():
    # buscar todos os times no banco
    # 1- montar o SELECT
    times_sql = select(Time)  # não é a lista de times ainda
    # 2- executar o SELECT
    times = db_session.execute(times_sql).scalars().all()  # agora sim é a lista
    return times
def salvar(nome, turma, responsavel):
    try:
        time_novo = Time(nome=nome, turma=turma, responsavel=responsavel)
        db_session.add(time_novo)
        db_session.commit()
        flash('Time cadastrado com sucesso', 'success')
    except SQLAlchemyError as e:
        db_session.rollback()
        flash('ocorreu um erro, tente novamente', 'error')
        print(f"Erro: {e}")
    except Exception as e:
        db_session.rollback()
        flash('ocorreu um erro, tente novamente', 'error')
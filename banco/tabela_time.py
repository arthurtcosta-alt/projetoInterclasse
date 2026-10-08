from flask import flash
from sqlalchemy import select, func
from sqlalchemy.exc import SQLAlchemyError

from database import Time, db_session, Jogador


def select_todos_times():
    # buscar todos os times no banco
    # 1- montar o SELECT
    times_sql = (
        select(Time, func.count(Jogador.id).label("jogadores"))
                 .outerjoin(Jogador, Jogador.time_id == Time.id)
                 .group_by(Time.id)
    )# não é a lista de times ainda
    # 2- executar o SELECT
    times = db_session.execute(times_sql).all()  # agora sim é a lista
    return times

def select_quantidade_total():
    times_sql = select(func.count(Time.id))
    quantidade_total = db_session.execute(times_sql).scalar()
    return quantidade_total
print(select_quantidade_total())
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
from flask import flash
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from database import Partida, db_session


def select_todas_partidas():
    partidas_sql = select(Partida)  # não é a lista de times ainda
    # 2- executar o SELECT
    partidas = db_session.execute(partidas_sql).scalars().all()  # agora sim é a lista
def salvar(time_casa_id, time_visitante_id, gols_casa, gols_visitante, data_partida):
    try:
        partida_nova = Partida(time_casa_id=time_casa_id, time_visitante_id=time_visitante_id, gols_casa=gols_casa,gols_visitante=gols_visitante, data_partida=data_partida)
        db_session.add(partida_nova)
        db_session.commit()
        flash('partida cadastrada com sucesso', 'success')
    except SQLAlchemyError as e:
        db_session.rollback()
        flash('ocorreu um erro, tente novamente', 'error')
        print(f"Erro: {e}")
    except Exception as e:
        db_session.rollback()
        flash('ocorreu um erro, tente novamente', 'error')
        print(f"Erro: {e}")
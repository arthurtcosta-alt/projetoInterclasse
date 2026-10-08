from flask import flash
from sqlalchemy import select, func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql.elements import or_
from sqlalchemy.orm import aliased

from database import Partida, db_session, Time


def select_todas_partidas():
    Timecasa = aliased (Time)
    Timevisitante = aliased (Time)
    partidas_sql = (select(Partida, Timecasa, Timevisitante)
                    .join(Timecasa,Partida.time_casa_id == Timecasa.id)
                    .join(Timevisitante,Partida.time_visitante_id == Timevisitante.id))
    # 2- executar o SELECT
    partidas_casa = db_session.execute(partidas_sql).all() # agora sim é a lista
    return partidas_casa
def select_quantidade_total():
    partidas_sql = select(func.count(Partida.id))
    quantidade_total = db_session.execute(partidas_sql).scalar()
    return quantidade_total
print(select_quantidade_total())
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
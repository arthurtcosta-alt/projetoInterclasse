from flask import flash
from sqlalchemy import select, func
from sqlalchemy.exc import SQLAlchemyError

from database import Partida, db_session, Jogador, Time


def select_todos_jogadores():
    # buscar todos os times no banco
    # 1- montar o SELECT
    # JOIN(Tabela que eu quero juntar, conidção --> chave estrangeira == chave primaira)
    jogadores_sql = select(Jogador, Time).join(Time, Jogador.time_id == Time.id)  # não é a lista de times ainda
    # 2- executar o SELECT
    # scalars só é utlizado quando tiver somente uma tabela --> dentro do parenteses do select da função ex: jogadores_sql
    jogadores = db_session.execute(jogadores_sql).all()  # agora sim é a lista
    return jogadores
def select_quantidade_total():
    jogadores_sql = select(func.count(Jogador.id))
    quantidade_total = db_session.execute(jogadores_sql).scalar()
    return quantidade_total
print(select_quantidade_total())
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

def select_um(id_jogador):
    jogador_sql = select(Jogador).where(Jogador.id == id_jogador)
    jogador = db_session.execute(jogador_sql).scalar_one_or_none()
    return jogador
print(select_um(10))
def select_por_time(id_time):
    jogador_sql = select(Jogador).where(id_time == Jogador.time_id)
    jogador = db_session.execute(jogador_sql).scalars().all()
    return jogador
print(select_por_time(1))
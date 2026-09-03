from typing import List, Optional

from src.database.conexao import conectar
from src.schemas.turmas import Turma, TurmaCadastro, TurmaEditar


def consultar_todos() -> List[Turma]:
    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute("SELECT id_turma, id_professor, id_curso, nome, horario, data_inicio, data_fim, vagas_totais FROM turmas")
            registros = cursor.fetchall()

    turmas = []
    for registro in registros:
        turma = Turma(id_turma=registro[0], id_professor=registro[1], id_curso=registro[2], nome=registro[3], horario=registro[4], data_inicio=registro[5], data_fim=registro[6], vagas_totais=registro[7])
        turmas.append(turma)
    return turmas


def cadastrar(turma: TurmaCadastro):
    sql = "INSERT INTO turmas (id_professor, id_curso, nome, horario, data_inicio, data_fim, vagas_totais) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(sql, (turma.id_professor, turma.id_curso, turma.nome, turma.horario, turma.data_inicio, turma.data_fim, turma.vagas_totais))
            novo_id = cursor.lastrowid
            conexao.commit()

    return Turma(id_turma=novo_id, id_professor=turma.id_professor, id_curso=turma.id_curso, nome=turma.nome, horario=turma.horario, data_inicio=turma.data_inicio, data_fim=turma.data_fim, vagas_totais=turma.vagas_totais)


def apagar(id_turma: int):
    sql = "DELETE FROM turmas WHERE id_turma = %s"
    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(sql, (id_turma,))
            conexao.commit()


def consultar_por_id(id_turma: int) -> Optional[Turma]:
    sql = "SELECT id_turma, id_professor, id_curso, nome, horario, data_inicio, data_fim, vagas_totais FROM turmas WHERE id_turma = %s"
    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(sql, (id_turma,))
            registro = cursor. fetchone()
    if registro is None:
        return None
    return Turma(id_turma=registro[0], id_professor=registro[1], id_curso=registro[2], nome=registro[3], horario=registro[4], data_inicio=registro[5], data_fim=registro[6], vagas_totais=registro[7])


def editar(id_turma: int, turma: TurmaEditar):
    sql = "UPDATE turmas SET id_professor = %s, id_curso = %s, nome = %s, horario = %s, data_inicio = %s, data_fim = %s, vagas_totais = %s"
    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(sql, (turma.id_professor, turma.id_curso, turma.nome, turma.horario, turma.data_inicio, turma.data_fim, turma.vagas_totais))
            conexao.commit()

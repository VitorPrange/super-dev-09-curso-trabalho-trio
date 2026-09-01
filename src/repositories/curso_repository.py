from typing import List, Optional

from src.database.conexao import conectar
from src.schemas.cursos import Curso, CursoCadastro, CursoEditar


def consultar_todos() -> List[Curso]:
    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute("SELECT id_curso, id_idioma, nome, nivel, carga_horaria, valor_mensalidade FROM cursos")
            registros = cursor.fetchall()

    cursos = []
    for registro in registros:
        curso = Curso(id=registro[0], id_idioma=registro[1], nome=registro[2], nivel=registro[3], carga_horario=registro[4], valor_mensalidade=registro[5])
        cursos.append(curso)
    return cursos


def cadastrar(curso: CursoCadastro):
    """Responsável por cadastrar o curso no banco de dados"""
    sql = "INSERT INTO cursos (id_idioma, nome, nivel, carga_horaria, valor_mensalidade) VALUES (%s, %s, %s, %s, %s)"
    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(sql, (curso.id_idioma, curso.nome, curso.nivel, curso.carga_horario, curso.valor_mensalidade))
            novo_id = cursor.lastrowid
            conexao.commit()

    return Curso(id=novo_id, id_idioma=curso.id_idioma, nome=curso.nome, nivel=curso.nivel, carga_horario=curso.carga_horario, valor_mensalidade=curso.valor_mensalidade)


def apagar(id: int):
    sql = "DELETE FROM cursos WHERE id_curso = %s"
    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(sql, (id,))
            conexao.commit()


def consultar_por_id(id: int) -> Optional[Curso]:
    sql = "SELECT id_curso, id_idioma, nome, nivel, carga_horaria, valor_mensalidade FROM cursos WHERE id_curso = %s"
    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(sql, (id,))
            registro = cursor.fetchone()
    if registro is None:
        return None
    return Curso(id=registro[0], id_idioma=registro[1], nome=registro[2], nivel=registro[3], carga_horario=registro[4], valor_mensalidade=registro[5])


def editar(id: int, curso: CursoEditar):
    sql = "UPDATE cursos SET id_idioma = %s, nome = %s, nivel = %s, carga_horaria = %s, valor_mensalidade = %s WHERE id_curso = %s"
    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(sql, (curso.id_idioma, curso.nome, curso.nivel, curso.carga_horario, curso.valor_mensalidade, id))
            conexao.commit()
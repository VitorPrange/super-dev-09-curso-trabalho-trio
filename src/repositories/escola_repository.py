from typing import Optional

from src.database.conexao import conectar
from src.schemas.escola import Escola, EscolaCadastro, EscolaEditar


def listar_escolas():
    sql = """SELECT id_escola AS `Id`,
cursos.id_curso AS `Id curso`,
escola.nome AS `Nome`,
escola.cnpj AS `CNPJ`,
escola.endereco AS `Endereço`,
escola.telefone AS `Telefone`,
escola.email AS `Email`
FROM escola
INNER JOIN cursos ON(escola.id_curso = cursos.id_curso) ORDER BY id_escola"""

    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(sql)
            registros = cursor.fetchall()
    
    escolas: list[Escola] = []

    for registro in registros:
        escola: Escola = Escola(
            id_escola=registro[0],
            id_curso=registro[1],
            nome=registro[2],
            cnpj=registro[3],
            endereco=registro[4],
            telefone=registro[5],
            email=registro[6],
        )

        escolas.append(escola)
    return escolas


def cadastrar_escola(escola: EscolaCadastro) -> Escola:
    sql = "INSERT INTO escola (id_curso, nome, cnpj, endereco, telefone, email) VALUES (%s, %s, %s, %s, %s, %s)"

    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(sql, (escola.id_curso, escola.nome, escola.cnpj, escola.endereco, escola.telefone, escola.email))
            novo_id = cursor.lastrowid
            conexao.commit()
    return Escola(
        id_escola=novo_id,
        id_curso=escola.id_curso,
        nome=escola.nome,
        cnpj=escola.cnpj,
        endereco=escola.endereco,
        telefone=escola.telefone,
        email=escola.email
    )


def apagar_escola(id_escola: int):
    sql = "DELETE FROM escola WHERE id_escola = %s"

    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(sql, (id_escola,))
            conexao.commit()


def editar_escola(id: int, escola:EscolaEditar):
    sql = """UPDATE escola SET
id_curso=%s,
nome=%s,
cnpj=%s,
endereco=%s,
telefone=%s,
email=%s
WHERE id_escola = %s"""

    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(sql, (escola.id_curso, escola.nome, escola.cnpj, escola.endereco, escola.telefone, escola.email, id))
            novo_id = cursor.lastrowid
            conexao.commit()


def consultar_por_id(id: int) -> Optional[Escola]:
    sql = """SELECT id_escola AS `Id`,
cursos.id_curso AS `Id curso`,
escola.nome AS `Nome`,
escola.cnpj AS `CNPJ`,
escola.endereco AS `Endereço`,
escola.telefone AS `Telefone`,
escola.email AS `Email`
FROM escola
INNER JOIN cursos ON(escola.id_curso = cursos.id_curso)
WHERE id_escola = %s
ORDER BY id_escola"""

    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(sql, (id,))
            registro = cursor.fetchone()
    
    if registro is None:
        return None

    escola: Escola = Escola(
        id_escola=registro[0],
        id_curso=registro[1],
        nome=registro[2],
        cnpj=registro[3],
        endereco=registro[4],
        telefone=registro[5],
        email=registro[6],
    )

    return escola
from dataclasses import dataclass
from typing import List, Optional

from src.database.conexao import conectar
from src.schemas.idiomas import Idioma, IdiomaCadastro, IdiomaEditar


def consultar_todos() -> List[Idioma]:
    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute("SELECT id, nome, descricao FROM idiomas")
            registros = cursor.fetchall()

    idiomas = []
    for registro in registros:
        idioma = Idioma(id=registro[0], nome=registro[1], descricao=registro[2])
        idiomas.append(idioma)
    return idiomas


def cadastrar(idioma: IdiomaCadastro):
    """Responsável por cadastrar o idioma no banco de dados"""
    sql = "INSERT INTO idiomas (nome, descricao) VALUES (%s, %s)"
    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(sql, (idioma.nome, idioma.descricao))
            novo_id = cursor.lastrowid
            conexao.commit()
    
    return Idioma(id=novo_id, nome=idioma.nome, descricao=idioma.descricao)


def apagar(id: int):
    """Responsável por apagar o idioma do banco de dados"""
    sql = "DELETE FROM idiomas WHERE id = %s"
    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(sql, (id,))
            conexao.commit()


def consultar_por_id(id: int) -> Optional[Idioma]:
    """Responsável por consultar o idioma filtrando por id"""
    sql = "SELECT id, nome, descricao FROM idiomas WHERE id = %s"
    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(sql, (id,))
            registro = cursor.fetchone()
    if registro is None:
        return None
    return Idioma(id=registro[0], nome=registro[1], descricao=registro[2])


def editar(id: int, idioma: IdiomaEditar):
    """Responsável por alterar os dados do idioma no banco de dados"""
    sql = "UPDATE idiomas SET nome = %s, descricao = %s WHERE id = %s"
    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(sql, (idioma.nome, idioma.descricao, id))
            conexao.commit()
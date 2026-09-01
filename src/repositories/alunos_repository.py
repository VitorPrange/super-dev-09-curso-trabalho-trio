import ssl
from typing import Optional

from src.database.conexao import conectar
from src.schemas.alunos import Aluno

def consultar_todos() -> list[Aluno]:
    sql = """SELECT
    alunos.id,
    alunos.nome,
    alunos.cpf,
    alunos.data_nascimento,
    alunos.email,
    alunos.telefone,
    alunos.data_cadastro
 """
    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(sql) 
            registros = cursor.fetchall()

    alunos: list[Aluno] = []
    for registro in registros:
        aluno: Aluno = Aluno(
            id=registro[0],
            nome=registro[1],
            cpf=registro[2],
            data_nascimento=registro[3],
            email=registro[4],
            telefone=registro[5],
            data_cadastro=registro[6]
        )

    alunos.append(aluno)
    return alunos


def cadastrar(aluno: AlunoCadastro) -> Aluno:
    sql = """INSERT INTO alunos
    (nome, cpf, data_nascimento, email, telefone, data_cadastro)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(sql, (aluno.nome, aluno.cpf, aluno.data_nascimento, aluno.email, aluno.telefone, aluno.data_cadastro))
            novo_id = cursor.lastrowid
            conexao.commit()
    return Aluno(
        id=novo_id,
        nome=aluno.nome,
        cpf=aluno.cpf,
        data_nascimento=aluno.data_nascimento,
        email=aluno.email,
        telefone=aluno.telefone,
        data_cadastro=aluno.data_cadastro
    )
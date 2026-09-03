from typing import Optional

from src.database.conexao import conectar
from src.schemas.alunos import Aluno, AlunoCadastro, AlunoEditar

def consultar_todos() -> list[Aluno]:
    sql = """SELECT 
        alunos.id_aluno AS `Id Aluno`,
        alunos.nome AS `Nome Aluno`,
        alunos.cpf AS `Cpf Aluno`,
        alunos.data_nascimento AS `Data Nascimento Aluno`,
        alunos.email AS `Email Aluno`,
        alunos.telefone AS `Telefone Aluno`,
        alunos.data_cadastro AS `Data Cadastro Aluno`
FROM alunos
ORDER BY id_aluno
"""
    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(sql) 
            registros = cursor.fetchall()

    alunos: list[Aluno] = []
    for registro in registros:
        aluno: Aluno = Aluno(
            id_aluno=registro[0],
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
        id_aluno=novo_id,
        nome=aluno.nome,
        cpf=aluno.cpf,
        data_nascimento=aluno.data_nascimento,
        email=aluno.email,
        telefone=aluno.telefone,
        data_cadastro=aluno.data_cadastro
    )

def editar(id: int, aluno: AlunoEditar):
    sql = """UPDATE alunos SET
        nome=%s,
        cpf=%s,
        data_nascimento=%s,
        email=%s,
        telefone=%s,
        data_cadastro=%s
    WHERE id_aluno=%s
    """

    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(sql, (
            aluno.nome,
            aluno.cpf,
            aluno.data_nascimento,
            aluno.email,
            aluno.telefone,
            aluno.data_cadastro,
            id
        ))
        conexao.commit()


def consultar_por_id(id: int) -> Optional[Aluno]:
    sql = """SELECT 
    alunos.id_aluno AS `Id Aluno`,
    alunos.nome AS `Nome Aluno`,
    alunos.cpf AS `Cpf Aluno`,
    alunos.data_nascimento AS `Data Nascimento Aluno`,
    alunos.email AS `Email Aluno`,
    alunos.telefone AS `Telefone Aluno`,
    alunos.data_cadastro AS `Data Cadastro Aluno`
FROM alunos
WHERE id_aluno=%s
ORDER BY id_aluno
"""
    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(sql, (id,))
            registro = cursor.fetchone()

    if registro is None:
        return None
    
    aluno: Aluno = Aluno(id_aluno=registro[0], 
        nome=registro[1],
        cpf=registro[2],
        data_nascimento=registro[3],
        email=registro[4],
        telefone=registro[5],
        data_cadastro=registro[6]
    )

    return aluno
    

def apagar(id_aluno: int):
    sql = "DELETE FROM alunos WHERE id_aluno = %s"
    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(sql, (id_aluno,))
            conexao.commit()
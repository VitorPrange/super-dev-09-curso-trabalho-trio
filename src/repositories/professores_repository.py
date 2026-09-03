from typing import Optional

from src.database.conexao import conectar
from src.schemas.professores import Professor, ProfessorCadastro, ProfessorEditar

def consultar_todos() -> list[Professor]:
    sql = """SELECT 
        professores.id_professor AS `Id professor`,
        professores.nome AS `Nome professor`,
        professores.cpf AS `Cpf professor`,        
        professores.email AS `Email professor`,
        professores.telefone AS `Telefone professor`,
        professores.formacao AS `Formacao professor`,
        professores.data_contratacao AS `Data Contratacao professor`
FROM professores
ORDER BY id_professor
"""
    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(sql) 
            registros = cursor.fetchall()

    professores: list[Professor] = []
    for registro in registros:
        professor: Professor = Professor(
            id_professor=registro[0],
            nome=registro[1],
            cpf=registro[2],
            email=registro[3],
            telefone=registro[4],
            formacao=registro[5],
            data_contratacao=registro[6]
        )
        professores.append(professor)
    return professores


def cadastrar(professor: ProfessorCadastro) -> Professor:
    sql = """INSERT INTO professores
    (nome, cpf, email, telefone, formacao, data_contratacao)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(sql, (professor.nome, professor.cpf, professor.email, professor.telefone,professor.formacao, professor.data_contratacao))
            novo_id = cursor.lastrowid
            conexao.commit()
    return Professor(
        id_professor=novo_id,
        nome=professor.nome,
        cpf=professor.cpf,
        email=professor.email,
        telefone=professor.telefone,
        formacao=professor.formacao,
        data_contratacao=professor.data_contratacao
    )

def editar(id: int, professor: ProfessorEditar):
    sql = """UPDATE professores SET
        nome=%s,
        cpf=%s,
        email=%s,
        telefone=%s,
        formacao=%s,
        data_contratacao=%s
    WHERE id_professor=%s
    """

    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(sql, (
            professor.nome,
            professor.cpf,
            professor.email,
            professor.telefone,
            professor.formacao,
            professor.data_contratacao,
            id
        ))
        conexao.commit()


def consultar_por_id(id: int) -> Optional[Professor]:
    sql = """SELECT 
            professores.id_professor AS `Id professor`,
            professores.nome AS `Nome professor`,
            professores.cpf AS `Cpf professor`,        
            professores.email AS `Email professor`,
            professores.telefone AS `Telefone professor`,
            professores.formacao AS `Formacao professor`,
            professores.data_contratacao AS `Data Contratacao professor`
    FROM professores
    WHERE id_professor=%s
    ORDER BY id_professor
    """
    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(sql, (id,))
            registro = cursor.fetchone()

    if registro is None:
        return None
    
    professor: Professor = Professor(id_professor=registro[0], 
        nome=registro[1],
        cpf=registro[2],
        email=registro[3],
        telefone=registro[4],
        formacao=registro[5],
        data_contratacao=registro[6]
    )

    return professor
    

def apagar(id_professor: int):
    sql = "DELETE FROM professores WHERE id_professor = %s"
    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(sql, (id_professor,))
            conexao.commit()
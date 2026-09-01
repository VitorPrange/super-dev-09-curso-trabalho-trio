from typing import Optional

from src.database.conexao import conectar
from src.schemas.matricula import Matricula, MatriculaCadastro, MatriculaEditar


def listar_matriculas():
    sql = """SELECT id_matricula AS `Id`,
alunos.id_aluno AS `Id Aluno`,
matriculas.id_turma AS `Id Turma`,
matriculas.data_matricula AS `Data Matricula`
FROM matriculas
INNER JOIN alunos ON(matriculas.id_aluno = alunos.id_aluno) ORDER BY id_matricula"""

    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(sql)
            registros = cursor.fetchall()
            
    matriculas: list[Matricula] = []
    
    for registro in registros:
        matricula: Matricula = Matricula(
            id_matricula=registro[0],
            id_aluno=registro[1],
            id_turma=registro[2],
            data_matricula=registro[3]
        )

        matriculas.append(matricula)
    return matriculas


def cadastrar_matricula(matricula: MatriculaCadastro) -> Matricula:
    sql = "INSERT INTO matriculas (id_aluno, id_turma, data_matricula) VALUES (%s, %s, %s)"
    
    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(sql, (matricula.id_aluno, matricula.id_turma, matricula.data_matricula))
            novo_id = cursor.lastrowid
            conexao.commit()
    return Matricula(
        id_matricula=novo_id,
        id_aluno=matricula.id_aluno,
        id_turma=matricula.id_turma,
        data_matricula=matricula.data_matricula
    )



def apagar_matricula(id_matricula: int):
    sql = "DELETE FROM matriculas WHERE id_matricula = %s"
    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(sql, (id_matricula,))
            conexao.commit()
            
            
def editar_matricula(id: int, matricula: MatriculaEditar):
    sql = """UPDATE matriculas SET
data_matricula=%s,
id_aluno=%s,
id_turma=%s
WHERE id_matricula =%s"""

    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(sql, (matricula.data_matricula, matricula.id_aluno, matricula.id_turma, id))
            conexao.commit()
            

def consultar_por_id(id: int) -> Optional[Matricula]:
    sql = """SELECT id_matricula AS `Id`,
alunos.id_aluno AS `Id Aluno`,
matriculas.id_turma AS `Id Turma`,
matriculas.data_matricula AS `Data Matricula`
FROM matriculas
INNER JOIN alunos ON(matriculas.id_aluno = alunos.id_aluno) 
WHERE id_matricula = %s
ORDER BY id_matricula"""

    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(sql, (id,))
            registro = cursor.fetchone()
            
    if registro is None:
        return None
    
    matricula: Matricula = Matricula(
        id_matricula=registro[0],
        id_aluno=registro[1],
        id_turma=registro[2],
        data_matricula=registro[3]
    )

    return matricula
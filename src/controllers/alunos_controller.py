from fastapi import APIRouter, HTTPException, status

from src.repositories import alunos_repository
from src.schemas.alunos import Aluno, AlunoCadastro, AlunoEditar

router: APIRouter = APIRouter(prefix="/alunos")


@router.get("")
def listar_alunos():
    return alunos_repository.consultar_todos()


@router.post("")
def cadastrar(aluno: AlunoCadastro):
    return alunos_repository.cadastrar(aluno)


@router.put("/{id}")
def editar(id: int, aluno: AlunoEditar):
    aluno_banco = alunos_repository.consultar_por_id(id)

    if aluno_banco is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aluno não encontrado")

    alunos_repository.editar(id, aluno)
    return {
        "status": "ok"
    }

@router.get("/{id}")
def consultar_por_id(id: int):
    aluno = alunos_repository.consultar_por_id(id)

    if aluno is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aluno não encontrado!!")

    return aluno


@router.delete("/{id}")
def apagar(id: int):
    aluno =  alunos_repository.consultar_por_id(id)

    if aluno is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aluno não encontrado")

    alunos_repository.apagar(id)
    return {
        "status": "ok"
    }
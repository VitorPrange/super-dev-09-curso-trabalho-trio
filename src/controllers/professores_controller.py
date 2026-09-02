from fastapi import APIRouter, HTTPException, status

from src.repositories import professores_repository
from src.schemas.professores import Professor, ProfessorCadastro, ProfessorEditar

router: APIRouter = APIRouter(prefix="/professores")


@router.get("")
def listar_professores():
    return professores_repository.consultar_todos()


@router.post("")
def cadastrar(professor: ProfessorCadastro):
    return professores_repository.cadastrar(professor)


@router.put("/{id}")
def editar(id: int, professor: ProfessorEditar):
    professor_banco = professores_repository.consultar_por_id(id)

    if professor_banco is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Professor não encontrado")

    professores_repository.editar(id, professor)
    return {
        "status": "ok"
    }

@router.get("/{id}")
def consultar_por_id(id: int):
    professor = professores_repository.consultar_por_id(id)

    if professor is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Professor não encontrado!!")

    return professor


@router.delete("/{id}")
def apagar(id: int):
    professor =  professores_repository.consultar_por_id(id)

    if professor is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Professor não encontrado")

    professores_repository.apagar(id)
    return {
        "status": "ok"
    }
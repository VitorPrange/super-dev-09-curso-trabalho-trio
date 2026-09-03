from fastapi import APIRouter, HTTPException, status

from src.repositories import turma_repository
from src.schemas.turmas import TurmaCadastro, TurmaEditar


router = APIRouter()

@router.get("/turmas")
def listar_turmas():
    return turma_repository.consultar_todos()


@router.post("/turmas")
def cadastrar_turma(turma: TurmaCadastro):
    return turma_repository.cadastrar(turma)


@router.delete("/turmas/{id}")
def apagar(id: int):
    turma_repository.apagar(id)
    return {"status": "OK"}


@router.get("/turmas/{id}")
def consultar_por_id(id: int):
    turma = turma_repository.consultar_por_id(id)
    if turma is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Turma não encontrada")

    return turma


@router.put("/turmas/{id}")
def editar(id: int, turma: TurmaEditar):
    turma_existente = turma_repository.consultar_por_id(id)
    if turma_existente is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Turma não encontrada")

    turma_repository.editar(id, turma)
    return{"status": "OK"}
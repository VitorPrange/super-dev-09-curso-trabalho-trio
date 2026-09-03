from fastapi import APIRouter, HTTPException, status

from src.repositories import curso_repository
from src.schemas.cursos import CursoCadastro, CursoEditar


router = APIRouter()


@router.get("/cursos")
def listar_cursos():
    return curso_repository.consultar_todos()


@router.post("/cursos")
def cadastrar_curso(curso: CursoCadastro):
    return curso_repository.cadastrar(curso)


@router.delete("/cursos/{id}")
def apagar(id: int):
    curso_repository.apagar(id)
    return {"status": "OK"}


@router.get("/cursos/{id}")
def consultar_por_id(id: int):
    curso = curso_repository.consultar_por_id(id)
    if curso is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Curso não encontrado")

    return curso


@router.put("/cursos/{id}")
def editar(id: int, curso: CursoEditar):
    curso_existente = curso_repository.consultar_por_id(id)
    if curso_existente is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Curso não encontrado")

    curso_repository.editar(id, curso)
    return {"status": "OK"} 
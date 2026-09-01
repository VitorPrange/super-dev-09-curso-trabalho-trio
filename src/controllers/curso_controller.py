from fastapi import APIRouter


router = APIRouter()


@router.get("/cursos")
def listar_cursos():
    return curso_repository.consultar_todos()


@router.post("/cursos")
def cadastrar_curso
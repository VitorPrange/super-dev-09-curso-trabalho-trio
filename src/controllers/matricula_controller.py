from fastapi import APIRouter, HTTPException, status

from src.repositories import matricula_repository
from src.schemas.matricula import Matricula, MatriculaCadastro, MatriculaEditar


router: APIRouter = APIRouter(prefix="/matriculas")

@router.get("")
def listar_matriculas():
    return matricula_repository.listar_matriculas()


@router.post("")
def cadastrar_matricula(matricula: MatriculaCadastro):
    return matricula_repository.cadastrar_matricula(matricula)


@router.delete("/{id}")
def apagar_matricula(id: int):
    matricula_repository.apagar_matricula(id)
    
    return {
        "status": "OK"
    }
    
    
@router.get("/{id}")
def consultar_por_id(id: int):
    matricula = matricula_repository.consultar_por_id(id)
    
    if matricula is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Matricula não encontrado")

    return matricula


@router.put("/{id}")
def editar_matricula(id: int, matricula: MatriculaEditar):
    matricula_banco = matricula_repository.consultar_por_id(id)

    if matricula_banco is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Matricula não encontrado")

    matricula_repository.editar_matricula(id, matricula)
    return {
        "status": "ok"
    }
    
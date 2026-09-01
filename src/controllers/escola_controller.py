from fastapi import APIRouter, HTTPException, status

from src.repositories import escola_repository
from src.schemas.escola import Escola, EscolaCadastro, EscolaEditar

router: APIRouter = APIRouter(prefix="/escola")


@router.get("")
def listar_escolas():
    return escola_repository.listar_escolas()


@router.post("")
def cadastrar_escola(escola: EscolaCadastro):
    return escola_repository.cadastrar_escola(escola)


@router.delete("/{id}")
def apagar_escola(id: int):
    escola_repository.apagar_escola(id)

    return {
        "status": "OK"
    }


@router.get("/{id}")
def consultar_por_id(id: int):
    escola = escola_repository.consultar_por_id(id)

    if escola is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Escola não encontrada")

    return escola


@router.put("/{id}")
def editar_escola(id: int, escola: EscolaEditar):
    escola_banco = escola_repository.consultar_por_id(id)

    if escola_banco is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Escola não encontrada")
    
    escola_repository.editar_escola(id, escola)
    return {
        "status": "OK"
    }

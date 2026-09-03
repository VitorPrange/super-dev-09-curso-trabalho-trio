from fastapi import APIRouter, HTTPException, status

from src.repositories import idioma_repository
from src.schemas.idiomas import IdiomaCadastro, IdiomaEditar


router = APIRouter()


@router.get("/idiomas")
def listar_idiomas():
    return idioma_repository.consultar_todos()


@router.post ("/idiomas")
def cadastrar_idioma(idioma: IdiomaCadastro):
    return idioma_repository.cadastrar(idioma)


@router.delete("/idiomas/{id}")
def apagar(id: int):
    idioma_repository.apagar(id)
    return {"status": "OK"}


@router.get("/idiomas/{id}")
def consultar_por_id(id: int):
    idioma = idioma_repository.consultar_por_id(id)
    if idioma is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Idioma não encotrado")
    
    return idioma


@router.put("/idiomas/{id}")
def editar(id: int, idioma: IdiomaEditar):
    idioma_existente = idioma_repository.consultar_por_id(id)
    if idioma_existente is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Idioma não encontrado")
    
    idioma_repository.editar(id, idioma)
    return {"status": "OK"}

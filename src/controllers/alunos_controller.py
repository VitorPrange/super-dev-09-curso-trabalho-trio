from fastapi import APIRouter, HTTPException, status

from src.repositories import alunos_repository
from src.schemas.alunos import AlunoCadastro, AlunoEditar

router: APIRouter = APIRouter(prefix="/alunos")

@router.get("")
def listar_alunos():
    return alunos_repository.consultar_todos()

@router.post("")
def cadastrar(aluno: AlunoCadastro):
    return alunos_repository.cadastrar(aluno)
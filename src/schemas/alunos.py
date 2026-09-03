from dataclasses import dataclass
from datetime import date

@dataclass 
class Aluno: 
    id_aluno: int
    nome: str
    cpf: str
    data_nascimento: date
    email: str
    telefone: str
    data_cadastro: date


@dataclass
class AlunoCadastro:
    nome: str
    cpf: str
    data_nascimento: date
    email: str
    telefone: str
    data_cadastro: date


@dataclass
class AlunoEditar:
    nome: str
    cpf: str
    data_nascimento: date
    email: str
    telefone: str
    data_cadastro: date
from dataclasses import dataclass

@dataclass 
class Aluno: 
    id: int
    nome: str
    cpf: str
    data_nascimento: str
    email: str
    telefone: str
    data_cadastro: str


@dataclass
class AlunoCadastro:
    nome: str
    cpf: str
    data_nascimento: str
    email: str
    telefone: str
    data_cadastro: str


@dataclass
class AlunoEditar:
    nome: str
    cpf: str
    data_nascimento: str
    email: str
    telefone: str
    data_cadastro: str
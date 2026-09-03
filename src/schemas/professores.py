from dataclasses import dataclass
from datetime import date

@dataclass 
class Professor: 
    id_professor: int
    nome: str
    cpf: str
    email: str
    telefone: str
    formacao: str
    data_contratacao: date

@dataclass
class ProfessorCadastro:
    nome: str
    cpf: str
    email: str
    telefone: str
    formacao: str
    data_contratacao: date
    


@dataclass
class ProfessorEditar:
    nome: str
    cpf: str
    email: str
    telefone: str
    formacao: str
    data_contratacao: date
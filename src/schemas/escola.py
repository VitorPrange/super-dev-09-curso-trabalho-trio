from dataclasses import dataclass


@dataclass
class Escola():
    id_escola: int
    id_curso: int
    nome: str
    cnpj: str
    endereco: str
    telefone: str
    email: str


@dataclass
class EscolaCadastro():
    id_curso: int
    nome: str
    cnpj: str
    endereco: str
    telefone: str
    email: str


@dataclass
class EscolaEditar():
    id_curso: int
    nome: str
    cnpj: str
    endereco: str
    telefone: str
    email: str

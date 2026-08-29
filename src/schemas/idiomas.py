from dataclasses import dataclass


@dataclass
class Idioma:
    id: int
    nome: str
    descricao: str

@dataclass
class IdiomaCadastro:
    nome: str
    descricao: str

@dataclass
class IdiomaEditar:
    nome: str
    descricao: str
from dataclasses import dataclass

@dataclass
class Curso:
    id: int
    id_idioma: int
    nome: str
    nivel: int
    carga_horario: int
    valor_mensalidade: float


@dataclass
class CursoCadastro:
    id_idioma: int
    nome: str
    nivel: int
    carga_horario: int
    valor_mensalidade: float


@dataclass
class CursoEditar:
    id_idioma: int
    nome: str
    nivel: int
    carga_horario: int
    valor_mensalidade: float
    
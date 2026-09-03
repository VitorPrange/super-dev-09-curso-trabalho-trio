from dataclasses import dataclass


@dataclass
class Turma:
    id_turma: int
    id_professor: int
    id_curso: int
    nome: str
    horario: str
    data_inicio: str
    data_fim: str
    vagas_totais: int


@dataclass
class TurmaCadastro:
    id_professor: int
    id_curso: int
    nome: str
    horario: str
    data_inicio: str
    data_fim: str
    vagas_totais: int


@dataclass
class TurmaEditar:
    id_professor: int
    id_curso: int
    nome: str
    horario: str
    data_inicio: str
    data_fim: str
    vagas_totais: int

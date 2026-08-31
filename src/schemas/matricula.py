from dataclasses import dataclass
from datetime import date


@dataclass
class Matricula:
    id_matricula: int
    data_matricula: date
    id_aluno: int
    id_turma: int
    
    
@dataclass
class MatriculaCadastro:
    data_matricula: date
    id_aluno: int
    id_turma: int
    
    
@dataclass
class MatriculaEditar:
    data_matricula: date
    id_aluno: int
    id_turma: int
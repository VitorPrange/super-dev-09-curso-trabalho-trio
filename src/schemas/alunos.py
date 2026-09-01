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
DROP DATABASE IF EXISTS trabalho_trio;

CREATE DATABASE trabalho_trio;

USE trabalho_trio;

CREATE TABLE idiomas(
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(40) NOT NULL,
    descricao TEXT
);

CREATE TABLE alunos (
    id_aluno INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cpf CHAR(11) NOT NULL UNIQUE,
    data_nascimento DATE NOT NULL,
    email VARCHAR(100) UNIQUE,
    telefone VARCHAR(20),
    data_cadastro DATE NOT NULL DEFAULT (CURRENT_DATE)
);

CREATE TABLE professores (
    id_professor INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cpf CHAR(11) NOT NULL UNIQUE,
    email VARCHAR(100) UNIQUE,
    telefone VARCHAR(20),
    formacao VARCHAR(100),
    data_contratacao DATE NOT NULL
);

CREATE TABLE cursos (
    id_curso INT AUTO_INCREMENT PRIMARY KEY,
    id_idioma INT NOT NULL,
    nome VARCHAR(100) NOT NULL,
    nivel INT NOT NULL,
    carga_horaria INT NOT NULL,
    valor_mensalidade DECIMAL(10,2) NOT NULL,

    FOREIGN KEY (id_idioma) REFERENCES idiomas(id)
);

CREATE TABLE escola (
    id_escola INT AUTO_INCREMENT PRIMARY KEY,
    id_curso INT NOT NULL,
    nome VARCHAR(100) NOT NULL,
    cnpj CHAR(14) NOT NULL UNIQUE,
    endereco VARCHAR(150),
    telefone VARCHAR(20),
    email VARCHAR(100),

    FOREIGN KEY (id_curso) REFERENCES cursos(id_curso)
);

CREATE TABLE turmas (
    id_turma INT AUTO_INCREMENT PRIMARY KEY,
    id_professor INT NOT NULL,
    id_curso INT NOT NULL,
    nome VARCHAR(50) NOT NULL,
    horario VARCHAR(50),
    data_inicio DATE NOT NULL,
    data_fim DATE,
    vagas_totais INT NOT NULL DEFAULT 20,
    FOREIGN KEY (id_professor) REFERENCES professores(id_professor),
    FOREIGN KEY (id_curso) REFERENCES cursos(id_curso)
);

CREATE TABLE matriculas (
    id_matricula INT AUTO_INCREMENT PRIMARY KEY,
    id_aluno INT NOT NULL,
    id_turma INT NOT NULL,
    data_matricula DATE NOT NULL,
    frequencia INT NOT NULL DEFAULT(0),

    FOREIGN KEY (id_aluno) REFERENCES alunos(id_aluno),
    FOREIGN KEY (id_turma) REFERENCES turmas(id_turma)
);
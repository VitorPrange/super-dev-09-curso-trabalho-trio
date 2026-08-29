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

    FOREIGN KEY (id_aluno) REFERENCES alunos(id_aluno),
    FOREIGN KEY (id_turma) REFERENCES turmas(id_turma)
);

CREATE TABLE frequencias (
    id_frequencia INT AUTO_INCREMENT PRIMARY KEY,
    id_matricula INT NOT NULL,
    data_aula DATE NOT NULL,
    presente BOOLEAN NOT NULL DEFAULT TRUE,
    observacao VARCHAR(255),

    FOREIGN KEY (id_matricula) REFERENCES matriculas(id_matricula)
);

INSERT INTO idiomas (nome, descricao) VALUES
('Ingles', 'Idioma mais procurado da escola'),
('Espanhol', 'Foco em conversacao'),
('Frances', 'Turmas para iniciantes e avancados'),
('Alemao', 'Curso voltado para intercambio'),
('Italiano', 'Curso com enfase em cultura e culinaria');

INSERT INTO alunos (nome, cpf, data_nascimento, email, telefone) VALUES
('Matheus Souza', '11122233344', '2001-03-12', 'matheus.souza@email.com', '47999990001'),
('Elias Costa', '22233344455', '1999-07-25', 'elias.costa@email.com', '47999990002'),
('Lucas Pereira', '33344455566', '2003-11-02', 'lucas.pereira@email.com', '47999990003'),
('Rafael Lima', '44455566677', '2000-05-18', 'rafael.lima@email.com', '47999990004'),
('Samuel Rocha', '55566677788', '2002-09-30', 'samuel.rocha@email.com', '47999990005');

INSERT INTO professores (nome, cpf, email, telefone, formacao, data_contratacao) VALUES
('Ana Beatriz', '66677788899', 'ana.beatriz@escola.com', '47988880001', 'Letras - Ingles', '2020-02-01'),
('Carlos Eduardo', '77788899900', 'carlos.eduardo@escola.com', '47988880002', 'Letras - Espanhol', '2019-08-15'),
('Marina Alves', '88899900011', 'marina.alves@escola.com', '47988880003', 'Letras - Frances', '2021-03-10'),
('Julia Fernandes', '99900011122', 'julia.fernandes@escola.com', '47988880004', 'Letras - Alemao', '2022-01-20'),
('Pedro Henrique', '00011122233', 'pedro.henrique@escola.com', '47988880005', 'Letras - Italiano', '2018-06-05');

INSERT INTO cursos (id_idioma, nome, nivel, carga_horaria, valor_mensalidade) VALUES
(1, 'Ingles Basico', 1, 60, 250.00),
(2, 'Espanhol Intermediario', 2, 80, 230.00),
(3, 'Frances Avancado', 3, 100, 280.00),
(4, 'Alemao Basico', 1, 60, 260.00),
(5, 'Italiano Intermediario', 2, 80, 240.00);

INSERT INTO turmas (id_professor, id_curso, nome, horario, data_inicio, data_fim, vagas_totais) VALUES
(1, 1, 'Turma A - Manha', 'Seg/Qua 08:00-09:30', '2026-02-02', NULL, 20),
(2, 2, 'Turma B - Noite', 'Ter/Qui 19:00-20:30', '2026-02-03', NULL, 15),
(3, 3, 'Turma C - Tarde', 'Seg/Qua 14:00-15:30', '2026-02-02', NULL, 12),
(4, 4, 'Turma D - Manha', 'Ter/Qui 08:00-09:30', '2026-02-03', NULL, 18),
(5, 5, 'Turma E - Noite', 'Seg/Qua 19:00-20:30', '2026-02-02', NULL, 20);

INSERT INTO matriculas (id_aluno, id_turma, data_matricula) VALUES
(1, 1, '2026-02-01'),
(2, 2, '2026-02-01'),
(3, 3, '2026-02-02'),
(4, 4, '2026-02-02'),
(5, 5, '2026-02-03');

INSERT INTO frequencias (id_matricula, data_aula, presente, observacao) VALUES
(1, '2026-02-02', TRUE, NULL),
(2, '2026-02-03', TRUE, NULL),
(3, '2026-02-02', FALSE, 'Faltou por motivo de saude'),
(4, '2026-02-03', TRUE, NULL),
(5, '2026-02-02', TRUE, 'Chegou atrasado');
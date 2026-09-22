CREATE TABLE IF NOT EXISTS usuario (
    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(150) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    tipo_usuario VARCHAR(30) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'ATIVO',
    data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS dispositivo (
    id_dispositivo INTEGER PRIMARY KEY AUTOINCREMENT,
    id_usuario INTEGER NOT NULL,
    identificador VARCHAR(150) NOT NULL,
    sistema_operacional VARCHAR(100),
    navegador VARCHAR(100),
    primeiro_acesso DATETIME DEFAULT CURRENT_TIMESTAMP,
    ultimo_acesso DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (id_usuario)
        REFERENCES usuario(id_usuario)
);

CREATE TABLE IF NOT EXISTS acesso (
    id_acesso INTEGER PRIMARY KEY AUTOINCREMENT,
    id_usuario INTEGER NOT NULL,
    id_dispositivo INTEGER,
    data_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
    ip_origem VARCHAR(45) NOT NULL,
    pais VARCHAR(100),
    cidade VARCHAR(100),
    resultado VARCHAR(30) NOT NULL,

    FOREIGN KEY (id_usuario)
        REFERENCES usuario(id_usuario),

    FOREIGN KEY (id_dispositivo)
        REFERENCES dispositivo(id_dispositivo)
);

CREATE TABLE IF NOT EXISTS regra_comportamental (
    id_regra INTEGER PRIMARY KEY AUTOINCREMENT,
    id_usuario INTEGER NOT NULL,
    horario_inicio TIME NOT NULL,
    horario_fim TIME NOT NULL,
    pais_principal VARCHAR(100),
    dispositivo_principal INTEGER,
    atualizado_em DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (id_usuario)
        REFERENCES usuario(id_usuario),

    FOREIGN KEY (dispositivo_principal)
        REFERENCES dispositivo(id_dispositivo)
);

CREATE TABLE IF NOT EXISTS analise_risco (
    id_analise INTEGER PRIMARY KEY AUTOINCREMENT,
    id_acesso INTEGER NOT NULL UNIQUE,
    pontuacao DECIMAL(5,2) NOT NULL,
    nivel_risco VARCHAR(20) NOT NULL,
    motivo TEXT,
    data_hora DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (id_acesso)
        REFERENCES acesso(id_acesso)
);

CREATE TABLE IF NOT EXISTS acao_seguranca (
    id_acao INTEGER PRIMARY KEY AUTOINCREMENT,
    id_analise INTEGER NOT NULL,
    tipo_acao VARCHAR(30) NOT NULL,
    descricao TEXT,
    data_hora DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (id_analise)
        REFERENCES analise_risco(id_analise)
);
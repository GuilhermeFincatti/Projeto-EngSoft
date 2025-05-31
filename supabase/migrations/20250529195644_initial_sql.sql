CREATE TABLE Pessoa (
    Nickname VARCHAR PRIMARY KEY,
    Email VARCHAR NOT NULL,
    Senha VARCHAR NOT NULL,
    Tipo VARCHAR NOT NULL
);

CREATE TABLE Educador (
    Nickname VARCHAR PRIMARY KEY REFERENCES Pessoa(Nickname) ON DELETE CASCADE,
    Cargo VARCHAR NOT NULL
);

CREATE TABLE Usuario (
    Nickname VARCHAR PRIMARY KEY REFERENCES Pessoa(Nickname) ON DELETE CASCADE,
    Ranking VARCHAR NOT NULL,
    QtdCartas INT DEFAULT 0
);

CREATE TABLE Adiciona (
    Usuario1 VARCHAR REFERENCES Usuario(Nickname) ON DELETE CASCADE,
    Usuario2 VARCHAR REFERENCES Usuario(Nickname) ON DELETE CASCADE,
    DataHora TIMESTAMP,
    Status VARCHAR,
    PRIMARY KEY (Usuario1, Usuario2)
);

CREATE TABLE Chat (
    Usuario1 VARCHAR REFERENCES Usuario(Nickname) ON DELETE CASCADE,
    Usuario2 VARCHAR REFERENCES Usuario(Nickname) ON DELETE CASCADE,
    PRIMARY KEY (Usuario1, Usuario2)
);

CREATE TABLE Carta (
    QRCode VARCHAR PRIMARY KEY,
    Raridade VARCHAR,
    Imagem TEXT,
    Audio TEXT,
    Localizacao TEXT
);

CREATE TABLE Mensagem (
    Remetente VARCHAR REFERENCES Usuario(Nickname) ON DELETE CASCADE,
    Destinatario VARCHAR REFERENCES Usuario(Nickname) ON DELETE CASCADE,
    DataHora TIMESTAMP,
    Texto TEXT,
    Carta VARCHAR REFERENCES Carta(QRCode) ON DELETE CASCADE, 
    PRIMARY KEY (Remetente, Destinatario, DataHora)
);

CREATE TABLE Missao (
    Codigo SERIAL PRIMARY KEY,
    DataInicio timestamp DEFAULT CURRENT_TIMESTAMP,
    DataFim timestamp,
    Tipo VARCHAR,
    Educador VARCHAR REFERENCES Educador(Nickname) ON DELETE CASCADE
);

CREATE TABLE ParticipaRaridade (
    Usuario VARCHAR REFERENCES Usuario(Nickname) ON DELETE CASCADE,
    Codigo INT REFERENCES Missao(Codigo) ON DELETE CASCADE,
    Status VARCHAR,
    PRIMARY KEY (Usuario, Codigo)
);

CREATE TABLE ParticipaQuantidade (
    Usuario VARCHAR REFERENCES Usuario(Nickname) ON DELETE CASCADE,
    Codigo INT REFERENCES Missao(Codigo) ON DELETE CASCADE,
    QtdColetadas INT,
    PRIMARY KEY (Usuario, Codigo)
);


CREATE TABLE CartaRara (
    QRCode VARCHAR PRIMARY KEY REFERENCES Carta(QRCode) ON DELETE CASCADE,
    Historia TEXT
);

CREATE TABLE MissaoRaridade (
    Codigo INT REFERENCES Missao(Codigo) ON DELETE CASCADE,
    CartaRara VARCHAR REFERENCES CartaRara(QRCode) ON DELETE CASCADE,
    PRIMARY KEY (Codigo, CartaRara)
);

CREATE TABLE MissaoQtd (
    Codigo INT REFERENCES Missao(Codigo) ON DELETE CASCADE,
    QuantidadeTotal INT,
    PRIMARY KEY (Codigo)
);


CREATE TABLE Coleta (
    Usuario VARCHAR REFERENCES Usuario(Nickname) ON DELETE CASCADE,
    QRCode VARCHAR REFERENCES Carta(QRCode) ON DELETE CASCADE,
    Quantidade INT,
    PRIMARY KEY (Usuario, QRCode)
);

CREATE TABLE MissaoQtdCartas (
    Codigo INT REFERENCES Missao(Codigo) ON DELETE CASCADE,
    QRCode VARCHAR REFERENCES Carta(QRCode) ON DELETE CASCADE,
    PRIMARY KEY (Codigo, QRCode)
);

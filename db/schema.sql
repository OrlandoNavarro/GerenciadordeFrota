-- Schema for fleet management
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE,
    full_name TEXT,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'operador',
    is_active INTEGER NOT NULL DEFAULT 1,
    created_at DATETIME DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS transporters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    razao_social TEXT NOT NULL,
    nome_fantasia TEXT,
    cnpj TEXT NOT NULL UNIQUE,
    inscricao_estadual TEXT,
    responsavel TEXT,
    telefone TEXT,
    email TEXT,
    endereco TEXT,
    cidade TEXT,
    estado TEXT,
    cep TEXT,
    status TEXT DEFAULT 'ativo',
    observacoes TEXT,
    validade_contrato DATE,
    seguradora TEXT,
    apolice TEXT,
    documento_anexo TEXT,
    tipo_operacao TEXT,
    created_at DATETIME DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS vehicles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    placa TEXT NOT NULL UNIQUE,
    tipo TEXT,
    modelo TEXT,
    marca TEXT,
    ano INTEGER,
    capacidade REAL,
    combustivel TEXT,
    consumo_medio REAL,
    status TEXT DEFAULT 'ativo',
    transporter_id INTEGER,
    observacoes TEXT,
    FOREIGN KEY(transporter_id) REFERENCES transporters(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS drivers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    cpf TEXT NOT NULL UNIQUE,
    cnh TEXT,
    categoria TEXT,
    validade_cnh DATE,
    telefone TEXT,
    email TEXT,
    transporter_id INTEGER,
    status TEXT DEFAULT 'ativo',
    observacoes TEXT,
    FOREIGN KEY(transporter_id) REFERENCES transporters(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS trips (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    origem TEXT,
    destino TEXT,
    data_saida DATE,
    data_prevista_chegada DATE,
    data_chegada DATE,
    motorista_id INTEGER,
    vehicle_id INTEGER,
    transporter_id INTEGER,
    tipo_carga TEXT,
    peso REAL,
    valor_frete REAL,
    status TEXT DEFAULT 'planejada',
    observacoes TEXT,
    FOREIGN KEY(motorista_id) REFERENCES drivers(id),
    FOREIGN KEY(vehicle_id) REFERENCES vehicles(id),
    FOREIGN KEY(transporter_id) REFERENCES transporters(id)
);

CREATE TABLE IF NOT EXISTS fuelings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data DATE,
    vehicle_id INTEGER,
    motorista_id INTEGER,
    posto TEXT,
    litros REAL,
    valor_total REAL,
    valor_por_litro REAL,
    km_atual REAL,
    observacoes TEXT,
    FOREIGN KEY(vehicle_id) REFERENCES vehicles(id),
    FOREIGN KEY(motorista_id) REFERENCES drivers(id)
);

CREATE TABLE IF NOT EXISTS maintenances (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vehicle_id INTEGER,
    tipo TEXT,
    data DATE,
    oficina TEXT,
    custo REAL,
    descricao TEXT,
    status TEXT DEFAULT 'aberto',
    proxima_revisao DATE,
    observacoes TEXT,
    FOREIGN KEY(vehicle_id) REFERENCES vehicles(id)
);

CREATE TABLE IF NOT EXISTS documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo_documento TEXT,
    categoria_referencia TEXT,
    referencia_id INTEGER,
    numero TEXT,
    data_emissao DATE,
    data_vencimento DATE,
    status TEXT DEFAULT 'vigente',
    observacoes TEXT
);

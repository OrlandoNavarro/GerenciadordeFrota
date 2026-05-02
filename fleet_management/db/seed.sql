-- Seed initial data for transporters and vehicles

INSERT OR IGNORE INTO transporters (razao_social, nome_fantasia, cnpj, cidade, estado, telefone, email, status)
VALUES
('Transporte Exemplo LTDA', 'TransEx', '12345678000199', 'São Paulo', 'SP', '+55 11 99999-0001', 'contato@transex.com', 'ativo'),
('Logística Demo SA', 'LogiDemo', '98765432000188', 'Campinas', 'SP', '+55 19 99999-0002', 'comercial@logidemo.com', 'ativo');

INSERT OR IGNORE INTO vehicles (placa, tipo, modelo, marca, ano, capacidade, combustivel, consumo_medio, status, transporter_id)
VALUES
('ABC1D23','Caminhão','FH','Volvo',2018,20.0,'Diesel',3.5,'ativo',1),
('XYZ9Z88','VUC','Delivery','Mercedes',2020,6.5,'Diesel',5.0,'ativo',2);

-- Seed initial data: transporters, vehicles, drivers, trips, fuelings, maintenances

-- Transporters (20)
INSERT OR IGNORE INTO transporters (razao_social, nome_fantasia, cnpj, cidade, estado, telefone, email, status, validade_contrato, seguradora, apolice)
VALUES
('Transportadora Exemplo 1 LTDA','TransEx 1','10000000000001','São Paulo','SP','+55 11 90001-0001','contato1@transportadora.com','ativo','2025-12-31','Seguradora A','APOLICE1001'),
('Transportadora Exemplo 2 LTDA','TransEx 2','10000000000002','Campinas','SP','+55 19 90001-0002','contato2@transportadora.com','ativo','2025-11-30','Seguradora B','APOLICE1002'),
('Transportadora Exemplo 3 LTDA','TransEx 3','10000000000003','Santos','SP','+55 13 90001-0003','contato3@transportadora.com','ativo','2026-01-15','Seguradora C','APOLICE1003'),
('Transportadora Exemplo 4 LTDA','TransEx 4','10000000000004','Ribeirão Preto','SP','+55 16 90001-0004','contato4@transportadora.com','ativo','2026-02-20','Seguradora D','APOLICE1004'),
('Transportadora Exemplo 5 LTDA','TransEx 5','10000000000005','São José dos Campos','SP','+55 12 90001-0005','contato5@transportadora.com','ativo','2026-03-10','Seguradora E','APOLICE1005'),
('Transportadora Exemplo 6 LTDA','TransEx 6','10000000000006','Sorocaba','SP','+55 15 90001-0006','contato6@transportadora.com','ativo','2026-04-01','Seguradora F','APOLICE1006'),
('Transportadora Exemplo 7 LTDA','TransEx 7','10000000000007','Jundiaí','SP','+55 11 90001-0007','contato7@transportadora.com','ativo','2025-09-30','Seguradora G','APOLICE1007'),
('Transportadora Exemplo 8 LTDA','TransEx 8','10000000000008','Piracicaba','SP','+55 19 90001-0008','contato8@transportadora.com','ativo','2025-10-31','Seguradora H','APOLICE1008'),
('Transportadora Exemplo 9 LTDA','TransEx 9','10000000000009','Bauru','SP','+55 14 90001-0009','contato9@transportadora.com','ativo','2026-05-20','Seguradora I','APOLICE1009'),
('Transportadora Exemplo 10 LTDA','TransEx 10','10000000000010','Limeira','SP','+55 19 90001-0010','contato10@transportadora.com','ativo','2026-06-15','Seguradora J','APOLICE1010'),
('Transportadora Exemplo 11 LTDA','TransEx 11','10000000000011','Fortaleza','CE','+55 85 90001-0011','contato11@transportadora.com','ativo','2025-08-01','Seguradora K','APOLICE1011'),
('Transportadora Exemplo 12 LTDA','TransEx 12','10000000000012','Recife','PE','+55 81 90001-0012','contato12@transportadora.com','ativo','2025-07-20','Seguradora L','APOLICE1012'),
('Transportadora Exemplo 13 LTDA','TransEx 13','10000000000013','Salvador','BA','+55 71 90001-0013','contato13@transportadora.com','ativo','2026-09-10','Seguradora M','APOLICE1013'),
('Transportadora Exemplo 14 LTDA','TransEx 14','10000000000014','Belo Horizonte','MG','+55 31 90001-0014','contato14@transportadora.com','ativo','2026-10-05','Seguradora N','APOLICE1014'),
('Transportadora Exemplo 15 LTDA','TransEx 15','10000000000015','Curitiba','PR','+55 41 90001-0015','contato15@transportadora.com','ativo','2027-01-20','Seguradora O','APOLICE1015'),
('Transportadora Exemplo 16 LTDA','TransEx 16','10000000000016','Porto Alegre','RS','+55 51 90001-0016','contato16@transportadora.com','ativo','2027-02-14','Seguradora P','APOLICE1016'),
('Transportadora Exemplo 17 LTDA','TransEx 17','10000000000017','Florianópolis','SC','+55 48 90001-0017','contato17@transportadora.com','ativo','2025-05-30','Seguradora Q','APOLICE1017'),
('Transportadora Exemplo 18 LTDA','TransEx 18','10000000000018','Manaus','AM','+55 92 90001-0018','contato18@transportadora.com','ativo','2025-04-25','Seguradora R','APOLICE1018'),
('Transportadora Exemplo 19 LTDA','TransEx 19','10000000000019','Belém','PA','+55 91 90001-0019','contato19@transportadora.com','ativo','2026-12-31','Seguradora S','APOLICE1019'),
('Transportadora Exemplo 20 LTDA','TransEx 20','10000000000020','Goiânia','GO','+55 62 90001-0020','contato20@transportadora.com','ativo','2026-07-15','Seguradora T','APOLICE1020');

-- Vehicles (20) - each linked to a transporter
INSERT OR IGNORE INTO vehicles (placa, tipo, modelo, marca, ano, capacidade, combustivel, consumo_medio, status, transporter_id, observacoes)
VALUES
('TRP0001','Caminhão','FH','Volvo',2018,20.0,'Diesel',3.5,'ativo',1,'Bem conservado'),
('TRP0002','VUC','Accelo','Mercedes',2020,6.5,'Diesel',5.0,'ativo',2,''),
('TRP0003','Carreta','FH','Scania',2016,30.0,'Diesel',2.8,'ativo',3,''),
('TRP0004','Van','Sprinter','Mercedes',2019,3.5,'Diesel',8.0,'ativo',4,''),
('TRP0005','Caminhão','NH','Iveco',2017,18.0,'Diesel',3.9,'ativo',5,''),
('TRP0006','Caminhão','FH','Volvo',2015,25.0,'Diesel',3.2,'ativo',6,''),
('TRP0007','VUC','Master','Renault',2021,5.5,'Diesel',6.5,'ativo',7,''),
('TRP0008','Carreta','G440','Scania',2014,33.0,'Diesel',2.6,'ativo',8,''),
('TRP0009','Van','Ducato','Fiat',2018,3.0,'Diesel',9.0,'ativo',9,''),
('TRP0010','Caminhão','FH','Volvo',2022,22.0,'Diesel',3.4,'ativo',10,''),
('TRP0011','Caminhão','Actros','Mercedes',2016,24.0,'Diesel',3.3,'ativo',11,''),
('TRP0012','Carreta','R450','Volvo',2019,28.0,'Diesel',2.9,'ativo',12,''),
('TRP0013','VUC','HR','Hyundai',2020,4.5,'Diesel',7.0,'ativo',13,''),
('TRP0014','Van','Sprinter','Mercedes',2017,3.8,'Diesel',8.5,'ativo',14,''),
('TRP0015','Caminhão','FH','Volvo',2013,20.0,'Diesel',3.7,'ativo',15,''),
('TRP0016','Carreta','G380','Scania',2015,32.0,'Diesel',2.7,'ativo',16,''),
('TRP0017','VUC','Fiorino','Fiat',2022,1.5,'Flex',12.0,'ativo',17,''),
('TRP0018','Caminhão','NH','Iveco',2014,19.0,'Diesel',4.0,'ativo',18,''),
('TRP0019','Van','Ducato','Fiat',2021,3.2,'Diesel',9.0,'ativo',19,''),
('TRP0020','Caminhão','FH','Volvo',2020,21.0,'Diesel',3.6,'ativo',20,'');

-- Drivers (20)
INSERT OR IGNORE INTO drivers (nome, cpf, cnh, categoria, validade_cnh, telefone, email, transporter_id, status, observacoes)
VALUES
('Motorista 1','10000000001','CNH0001','C','2026-05-01','+55 11 90001-1001','motorista1@empresa.com',1,'ativo',''),
('Motorista 2','10000000002','CNH0002','C','2025-10-10','+55 19 90001-1002','motorista2@empresa.com',2,'ativo',''),
('Motorista 3','10000000003','CNH0003','D','2027-01-20','+55 13 90001-1003','motorista3@empresa.com',3,'ativo',''),
('Motorista 4','10000000004','CNH0004','C','2026-03-15','+55 16 90001-1004','motorista4@empresa.com',4,'ativo',''),
('Motorista 5','10000000005','CNH0005','C','2026-07-30','+55 12 90001-1005','motorista5@empresa.com',5,'ativo',''),
('Motorista 6','10000000006','CNH0006','C','2025-09-05','+55 15 90001-1006','motorista6@empresa.com',6,'ativo',''),
('Motorista 7','10000000007','CNH0007','D','2028-02-11','+55 11 90001-1007','motorista7@empresa.com',7,'ativo',''),
('Motorista 8','10000000008','CNH0008','C','2027-06-22','+55 19 90001-1008','motorista8@empresa.com',8,'ativo',''),
('Motorista 9','10000000009','CNH0009','C','2026-12-01','+55 14 90001-1009','motorista9@empresa.com',9,'ativo',''),
('Motorista 10','10000000010','CNH0010','C','2027-03-03','+55 19 90001-1010','motorista10@empresa.com',10,'ativo',''),
('Motorista 11','10000000011','CNH0011','C','2025-11-11','+55 85 90001-1011','motorista11@empresa.com',11,'ativo',''),
('Motorista 12','10000000012','CNH0012','C','2026-01-01','+55 81 90001-1012','motorista12@empresa.com',12,'ativo',''),
('Motorista 13','10000000013','CNH0013','D','2027-09-09','+55 71 90001-1013','motorista13@empresa.com',13,'ativo',''),
('Motorista 14','10000000014','CNH0014','C','2026-10-10','+55 31 90001-1014','motorista14@empresa.com',14,'ativo',''),
('Motorista 15','10000000015','CNH0015','C','2026-08-08','+55 41 90001-1015','motorista15@empresa.com',15,'ativo',''),
('Motorista 16','10000000016','CNH0016','C','2025-06-06','+55 51 90001-1016','motorista16@empresa.com',16,'ativo',''),
('Motorista 17','10000000017','CNH0017','C','2027-04-04','+55 48 90001-1017','motorista17@empresa.com',17,'ativo',''),
('Motorista 18','10000000018','CNH0018','C','2026-02-02','+55 92 90001-1018','motorista18@empresa.com',18,'ativo',''),
('Motorista 19','10000000019','CNH0019','C','2025-12-12','+55 91 90001-1019','motorista19@empresa.com',19,'ativo',''),
('Motorista 20','10000000020','CNH0020','D','2027-08-20','+55 62 90001-1020','motorista20@empresa.com',20,'ativo','');

-- Trips (20)
INSERT INTO trips (origem, destino, data_saida, data_prevista_chegada, data_chegada, motorista_id, vehicle_id, transporter_id, tipo_carga, peso, custo, status, observacoes)
VALUES
('São Paulo','Rio de Janeiro','2024-01-05','2024-01-07','2024-01-07',1,1,1,'Carga Geral',1200.0,800.0,'concluida',''),
('Campinas','Belo Horizonte','2024-01-10','2024-01-13','2024-01-13',2,2,2,'Refrigerada',1500.0,950.0,'concluida',''),
('Santos','Porto Alegre','2024-02-01','2024-02-06',NULL,3,3,3,'Carga Seca',2200.0,1300.0,'em andamento',''),
('Ribeirão Preto','Curitiba','2024-02-15','2024-02-18','2024-02-18',4,4,4,'Carga Geral',900.0,600.0,'concluida',''),
('São José dos Campos','Salvador','2024-03-01','2024-03-07',NULL,5,5,5,'Frigorificada',2000.0,1400.0,'planejada',''),
('Sorocaba','Fortaleza','2024-03-10','2024-03-17',NULL,6,6,6,'Carga Geral',1800.0,1200.0,'planejada',''),
('Jundiaí','Recife','2024-04-01','2024-04-08',NULL,7,7,7,'Carga Seca',1600.0,1100.0,'planejada',''),
('Piracicaba','Manaus','2024-04-12','2024-04-22',NULL,8,8,8,'Carga Geral',3000.0,2500.0,'planejada',''),
('Bauru','Belém','2024-05-05','2024-05-12',NULL,9,9,9,'Granel',4000.0,3000.0,'planejada',''),
('Limeira','Goiânia','2024-05-20','2024-05-23','2024-05-23',10,10,10,'Carga Geral',1100.0,700.0,'concluida',''),
('Fortaleza','João Pessoa','2024-06-01','2024-06-03','2024-06-03',11,11,11,'Carga Geral',950.0,650.0,'concluida',''),
('Recife','Maceió','2024-06-10','2024-06-12',NULL,12,12,12,'Carga Seca',850.0,500.0,'planejada',''),
('Salvador','Vitória','2024-06-20','2024-06-24',NULL,13,13,13,'Carga Geral',1300.0,900.0,'planejada',''),
('Belo Horizonte','Bauru','2024-07-01','2024-07-04',NULL,14,14,14,'Carga Geral',1250.0,880.0,'planejada',''),
('Curitiba','Florianópolis','2024-07-10','2024-07-11','2024-07-11',15,15,15,'Carga Leve',400.0,250.0,'concluida',''),
('Porto Alegre','Caxias do Sul','2024-07-20','2024-07-21',NULL,16,16,16,'Carga Geral',700.0,420.0,'planejada',''),
('Florianópolis','Joinville','2024-08-01','2024-08-02','2024-08-02',17,17,17,'Carga Leve',350.0,200.0,'concluida',''),
('Manaus','Boa Vista','2024-08-15','2024-08-18',NULL,18,18,18,'Carga Geral',2100.0,1600.0,'planejada',''),
('Belém','Macapá','2024-09-01','2024-09-04',NULL,19,19,19,'Carga Geral',1750.0,1150.0,'planejada',''),
('Campinas','Curitiba','2024-06-10','2024-06-13',NULL,20,20,20,'Frigorificada',2200.0,1500.0,'planejada','');

-- Fuelings (20)
INSERT INTO fuelings (data, vehicle_id, motorista_id, posto, litros, valor_total, valor_por_litro, km_atual, observacoes)
VALUES
('2024-02-10',1,1,'Posto A',150.0,600.0,4.0,125000.0,''),
('2024-02-12',2,2,'Posto B',80.0,320.0,4.0,98000.0,''),
('2024-03-01',3,3,'Posto C',200.0,900.0,4.5,210000.0,''),
('2024-03-05',4,4,'Posto D',60.0,270.0,4.5,150000.0,''),
('2024-03-10',5,5,'Posto E',120.0,540.0,4.5,175000.0,''),
('2024-04-01',6,6,'Posto F',160.0,720.0,4.5,190000.0,''),
('2024-04-12',7,7,'Posto G',45.0,180.0,4.0,85000.0,''),
('2024-04-20',8,8,'Posto H',220.0,990.0,4.5,230000.0,''),
('2024-05-02',9,9,'Posto I',50.0,225.0,4.5,112000.0,''),
('2024-05-12',10,10,'Posto J',140.0,630.0,4.5,132500.0,''),
('2024-05-20',11,11,'Posto K',130.0,585.0,4.5,142000.0,''),
('2024-06-01',12,12,'Posto L',90.0,405.0,4.5,156000.0,''),
('2024-06-10',13,13,'Posto M',55.0,247.5,4.5,98000.0,''),
('2024-06-20',14,14,'Posto N',70.0,315.0,4.5,176000.0,''),
('2024-07-01',15,15,'Posto O',180.0,810.0,4.5,200000.0,''),
('2024-07-10',16,16,'Posto P',210.0,945.0,4.5,225000.0,''),
('2024-07-20',17,17,'Posto Q',30.0,135.0,4.5,60000.0,''),
('2024-08-01',18,18,'Posto R',170.0,765.0,4.5,185000.0,''),
('2024-08-10',19,19,'Posto S',95.0,427.5,4.5,120000.0,''),
('2024-08-20',20,20,'Posto T',80.0,360.0,4.5,98000.0,'');

-- Maintenances (20)
INSERT INTO maintenances (vehicle_id, tipo, data, oficina, custo, descricao, status, proxima_revisao, observacoes)
VALUES
(1,'Troca de óleo','2024-03-01','Oficina A',250.0,'Troca de óleo e filtro','concluida','2024-09-01',''),
(2,'Pneus','2024-04-05','Oficina B',1200.0,'Troca de pneus dianteiros','concluida','2025-04-05',''),
(3,'Freios','2024-05-10','Oficina C',800.0,'Substituição de pastilhas','concluida','2024-11-10',''),
(4,'Alinhamento','2024-06-01','Oficina D',200.0,'Alinhamento e balanceamento','concluida','2024-12-01',''),
(5,'Troca de óleo','2024-06-15','Oficina E',300.0,'Troca de óleo','aberto','2024-12-15',''),
(6,'Suspensão','2024-07-01','Oficina F',950.0,'Reparo suspensão traseira','aberto','2025-01-01',''),
(7,'Freios','2024-07-10','Oficina G',600.0,'Reparo sistema de freios','concluida','2025-01-10',''),
(8,'Correia','2024-08-01','Oficina H',400.0,'Troca de correia dentada','agendado','2025-02-01',''),
(9,'Troca de óleo','2024-08-15','Oficina I',220.0,'Troca de óleo e filtro','concluida','2025-02-15',''),
(10,'Pneus','2024-09-01','Oficina J',1300.0,'Troca de pneus','agendado','2025-03-01',''),
(11,'Freios','2024-09-10','Oficina K',750.0,'Reparo freios','aberto','2025-03-10',''),
(12,'Troca de óleo','2024-10-01','Oficina L',260.0,'Troca de óleo','concluida','2025-04-01',''),
(13,'Suspensão','2024-10-15','Oficina M',980.0,'Reparo suspensão','agendado','2025-04-15',''),
(14,'Alinhamento','2024-11-01','Oficina N',210.0,'Alinhamento e balanceamento','concluida','2025-05-01',''),
(15,'Troca de óleo','2024-11-10','Oficina O',240.0,'Troca de óleo','concluida','2025-05-10',''),
(16,'Correia','2024-12-01','Oficina P',420.0,'Troca de correia','agendado','2025-06-01',''),
(17,'Freios','2024-12-10','Oficina Q',680.0,'Substituição pastilhas','agendado','2025-06-10',''),
(18,'Troca de óleo','2025-01-05','Oficina R',230.0,'Troca de óleo','concluida','2025-07-05',''),
(19,'Pneus','2025-02-01','Oficina S',1100.0,'Troca de pneus traseiros','agendado','2025-08-01',''),
(20,'Freios','2024-11-01','Oficina T',800.0,'Reparo sistema de freios','agendado','2025-05-01','');

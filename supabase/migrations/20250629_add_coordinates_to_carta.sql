-- Adicionar colunas de coordenadas à tabela carta
-- Execute este comando no seu banco de dados Supabase

ALTER TABLE carta 
ADD COLUMN IF NOT EXISTS latitude NUMERIC,
ADD COLUMN IF NOT EXISTS longitude NUMERIC;

-- Atualizar cartas existentes com coordenadas baseadas na localização
UPDATE carta SET latitude = -22.7085, longitude = -47.6305 WHERE localizacao = 'Prédio Principal - ESALQ';
UPDATE carta SET latitude = -22.7090, longitude = -47.6320 WHERE localizacao = 'Biblioteca Central';
UPDATE carta SET latitude = -22.7080, longitude = -47.6290 WHERE localizacao = 'Departamento de Ciências Exatas';
UPDATE carta SET latitude = -22.7095, longitude = -47.6310 WHERE localizacao = 'Jardim Botânico';
UPDATE carta SET latitude = -22.7075, longitude = -47.6325 WHERE localizacao = 'Museu de Mineralogia';
UPDATE carta SET latitude = -22.7100, longitude = -47.6300 WHERE localizacao = 'Departamento de Solos';
UPDATE carta SET latitude = -22.7070, longitude = -47.6315 WHERE localizacao = 'Observatório Astronômico';
UPDATE carta SET latitude = -22.7065, longitude = -47.6330 WHERE localizacao = 'Planetário ESALQ';
UPDATE carta SET latitude = -22.7088, longitude = -47.6295 WHERE localizacao = 'Laboratório de Física';
UPDATE carta SET latitude = -22.7092, longitude = -47.6285 WHERE localizacao = 'Centro de Pesquisas';
UPDATE carta SET latitude = -22.7078, longitude = -47.6340 WHERE localizacao = 'Museu de História Natural';

-- Comentário: As coordenadas foram definidas para localizações dentro da ESALQ
-- Estas coordenadas representam pontos aproximados dentro do campus da ESALQ-USP

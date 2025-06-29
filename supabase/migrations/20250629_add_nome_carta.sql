-- Adicionar campo nome à tabela carta
ALTER TABLE carta ADD COLUMN nome VARCHAR(255);

-- Atualizar cartas existentes com nomes baseados na localização e tipo
UPDATE carta SET nome = 
  CASE 
    WHEN qrcode = 'QR001' THEN 'Framboyant Dourado'
    WHEN qrcode = 'QR002' THEN 'Pau-Brasil Histórico'
    WHEN qrcode = 'QR003' THEN 'Pau-Formiga Guardião'
    WHEN qrcode = 'QR004' THEN 'Cuieté Majestoso'
    WHEN qrcode = 'QR005' THEN 'Abricó-de-Macaco'
    WHEN qrcode = 'QR006' THEN 'Sol Radiante'
    WHEN qrcode = 'QR007' THEN 'Júpiter Colossal'
    WHEN qrcode = 'QR008' THEN 'Saturno dos Anéis'
    WHEN qrcode = 'QR009' THEN 'Urano Místico'
    WHEN qrcode = 'QR010' THEN 'Netuno Tempestuoso'
    WHEN qrcode = 'QR011' THEN 'Plutão Distante'
    ELSE CONCAT('Carta ', qrcode)
  END;

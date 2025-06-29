-- Criar tabela de amizades
CREATE TABLE IF NOT EXISTS amizade (
    id SERIAL PRIMARY KEY,
    solicitante VARCHAR(50) NOT NULL REFERENCES usuario(nickname) ON DELETE CASCADE,
    destinatario VARCHAR(50) NOT NULL REFERENCES usuario(nickname) ON DELETE CASCADE,
    status VARCHAR(20) NOT NULL DEFAULT 'pendente' CHECK (status IN ('pendente', 'aceito', 'recusado')),
    data_solicitacao TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    data_aceite TIMESTAMP WITH TIME ZONE NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Constraints
    CONSTRAINT amizade_unique_pair UNIQUE (solicitante, destinatario),
    CONSTRAINT amizade_no_self CHECK (solicitante != destinatario)
);

-- Índices para melhor performance
CREATE INDEX IF NOT EXISTS idx_amizade_solicitante ON amizade(solicitante);
CREATE INDEX IF NOT EXISTS idx_amizade_destinatario ON amizade(destinatario);
CREATE INDEX IF NOT EXISTS idx_amizade_status ON amizade(status);

-- Trigger para atualizar updated_at
CREATE OR REPLACE FUNCTION update_amizade_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_amizade_updated_at
    BEFORE UPDATE ON amizade
    FOR EACH ROW
    EXECUTE FUNCTION update_amizade_updated_at();

-- Comentários
COMMENT ON TABLE amizade IS 'Tabela para gerenciar amizades entre usuários';
COMMENT ON COLUMN amizade.status IS 'Status da solicitação: pendente, aceito, recusado';
COMMENT ON COLUMN amizade.data_solicitacao IS 'Data em que a solicitação foi enviada';
COMMENT ON COLUMN amizade.data_aceite IS 'Data em que a solicitação foi aceita (se aplicável)';

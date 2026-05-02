from sqlalchemy import Column, Integer, String, Date, Text, DateTime
from db.connection import Base
from datetime import datetime


class Transporter(Base):
    __tablename__ = 'transporters'

    id = Column(Integer, primary_key=True, index=True)
    razao_social = Column(String, nullable=False)
    nome_fantasia = Column(String, nullable=True)
    cnpj = Column(String, nullable=False, unique=True, index=True)
    inscricao_estadual = Column(String, nullable=True)
    responsavel = Column(String, nullable=True)
    telefone = Column(String, nullable=True)
    email = Column(String, nullable=True)
    endereco = Column(String, nullable=True)
    cidade = Column(String, nullable=True)
    estado = Column(String, nullable=True)
    cep = Column(String, nullable=True)
    status = Column(String, default='ativo')
    observacoes = Column(Text, nullable=True)
    validade_contrato = Column(Date, nullable=True)
    seguradora = Column(String, nullable=True)
    apolice = Column(String, nullable=True)
    documento_anexo = Column(String, nullable=True)
    tipo_operacao = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'razao_social': self.razao_social,
            'nome_fantasia': self.nome_fantasia,
            'cnpj': self.cnpj,
            'responsavel': self.responsavel,
            'telefone': self.telefone,
            'email': self.email,
            'cidade': self.cidade,
            'estado': self.estado,
            'status': self.status,
            'observacoes': self.observacoes,
        }

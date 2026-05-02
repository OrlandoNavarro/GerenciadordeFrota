from sqlalchemy import Column, Integer, String, Date, Text
from db.connection import Base


class Document(Base):
    __tablename__ = 'documents'

    id = Column(Integer, primary_key=True, index=True)
    tipo_documento = Column(String, nullable=True)
    categoria_referencia = Column(String, nullable=True)
    referencia_id = Column(Integer, nullable=True)
    numero = Column(String, nullable=True)
    data_emissao = Column(Date, nullable=True)
    data_vencimento = Column(Date, nullable=True)
    status = Column(String, default='vigente')
    observacoes = Column(Text, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'tipo_documento': self.tipo_documento,
            'numero': self.numero,
            'status': self.status,
        }

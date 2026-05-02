from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey
from db.connection import Base


class Driver(Base):
    __tablename__ = 'drivers'

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    cpf = Column(String, unique=True, nullable=False, index=True)
    cnh = Column(String, nullable=True)
    categoria = Column(String, nullable=True)
    validade_cnh = Column(Date, nullable=True)
    telefone = Column(String, nullable=True)
    email = Column(String, nullable=True)
    transporter_id = Column(Integer, ForeignKey('transporters.id'), nullable=True)
    status = Column(String, default='ativo')
    observacoes = Column(Text, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'cpf': self.cpf,
            'cnh': self.cnh,
            'status': self.status,
        }

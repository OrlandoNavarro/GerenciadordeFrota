from sqlalchemy import Column, Integer, String, Float, Text
from sqlalchemy import ForeignKey
from db.connection import Base


class Vehicle(Base):
    __tablename__ = 'vehicles'

    id = Column(Integer, primary_key=True, index=True)
    placa = Column(String, unique=True, nullable=False, index=True)
    tipo = Column(String, nullable=True)
    modelo = Column(String, nullable=True)
    marca = Column(String, nullable=True)
    ano = Column(Integer, nullable=True)
    capacidade = Column(Float, nullable=True)
    combustivel = Column(String, nullable=True)
    consumo_medio = Column(Float, nullable=True)
    status = Column(String, default='ativo')
    transporter_id = Column(Integer, ForeignKey('transporters.id'), nullable=True)
    observacoes = Column(Text, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'placa': self.placa,
            'modelo': self.modelo,
            'marca': self.marca,
            'ano': self.ano,
            'status': self.status,
        }

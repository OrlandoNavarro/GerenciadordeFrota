from sqlalchemy import Column, Integer, String, Float, Date, Text, ForeignKey
from db.connection import Base


class Fueling(Base):
    __tablename__ = 'fuelings'

    id = Column(Integer, primary_key=True, index=True)
    data = Column(Date, nullable=True)
    vehicle_id = Column(Integer, ForeignKey('vehicles.id'), nullable=True)
    motorista_id = Column(Integer, ForeignKey('drivers.id'), nullable=True)
    posto = Column(String, nullable=True)
    litros = Column(Float, nullable=True)
    valor_total = Column(Float, nullable=True)
    valor_por_litro = Column(Float, nullable=True)
    km_atual = Column(Float, nullable=True)
    observacoes = Column(Text, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'data': self.data,
            'litros': self.litros,
            'valor_total': self.valor_total,
        }

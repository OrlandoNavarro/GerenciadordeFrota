from sqlalchemy import Column, Integer, String, Float, Date, Text, ForeignKey
from db.connection import Base


class Maintenance(Base):
    __tablename__ = 'maintenances'

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey('vehicles.id'), nullable=True)
    tipo = Column(String, nullable=True)
    data = Column(Date, nullable=True)
    oficina = Column(String, nullable=True)
    custo = Column(Float, nullable=True)
    descricao = Column(Text, nullable=True)
    status = Column(String, default='aberto')
    proxima_revisao = Column(Date, nullable=True)
    observacoes = Column(Text, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'vehicle_id': self.vehicle_id,
            'tipo': self.tipo,
            'status': self.status,
        }

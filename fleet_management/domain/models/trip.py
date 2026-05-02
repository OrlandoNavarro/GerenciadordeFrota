from sqlalchemy import Column, Integer, String, Float, Date, Text, ForeignKey
from db.connection import Base


class Trip(Base):
    __tablename__ = 'trips'

    id = Column(Integer, primary_key=True, index=True)
    origem = Column(String, nullable=True)
    destino = Column(String, nullable=True)
    data_saida = Column(Date, nullable=True)
    data_prevista_chegada = Column(Date, nullable=True)
    data_chegada = Column(Date, nullable=True)
    motorista_id = Column(Integer, ForeignKey('drivers.id'), nullable=True)
    vehicle_id = Column(Integer, ForeignKey('vehicles.id'), nullable=True)
    transporter_id = Column(Integer, ForeignKey('transporters.id'), nullable=True)
    tipo_carga = Column(String, nullable=True)
    peso = Column(Float, nullable=True)
    custo = Column(Float, nullable=True)
    status = Column(String, default='planejada')
    observacoes = Column(Text, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'origem': self.origem,
            'destino': self.destino,
            'status': self.status,
        }

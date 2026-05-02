import streamlit as st
import pandas as pd
from config.database import SessionLocal
from domain.services.transporter_service import TransporterService
from domain.services.driver_service import DriverService
from domain.services.vehicle_service import VehicleService
from domain.services.trip_service import TripService
from domain.services.fueling_service import FuelingService
from domain.services.maintenance_service import MaintenanceService


def render_toolbar():
    """Renderiza uma barra horizontal com ação 'Ver todos os dados'.
    Ao ativar, mostra uma tabela com contagens por entidade.
    """
    cols = st.columns([1, 8])
    with cols[0]:
        if st.button('Ver todos os dados', key='view_all_data_button'):
            st.session_state['show_all_data'] = not st.session_state.get('show_all_data', False)
    with cols[1]:
        pass

    if st.session_state.get('show_all_data'):
        with st.expander('Dados completos (contagens)'):
            db = SessionLocal()
            try:
                tsvc = TransporterService(db)
                dsvc = DriverService(db)
                vsvc = VehicleService(db)
                tripsvc = TripService(db)
                fsvc = FuelingService(db)
                msvc = MaintenanceService(db)

                data = [
                    {'Entidade': 'Transportadoras', 'Registros': len(tsvc.list_transporters())},
                    {'Entidade': 'Motoristas', 'Registros': len(dsvc.list_drivers())},
                    {'Entidade': 'Veículos', 'Registros': len(vsvc.list_vehicles())},
                    {'Entidade': 'Viagens', 'Registros': len(tripsvc.list_trips())},
                    {'Entidade': 'Abastecimentos', 'Registros': len(fsvc.list_fuelings())},
                    {'Entidade': 'Manutenções', 'Registros': len(msvc.list_maintenances())},
                ]
                df = pd.DataFrame(data)
                st.table(df)
            finally:
                try:
                    db.close()
                except Exception:
                    pass

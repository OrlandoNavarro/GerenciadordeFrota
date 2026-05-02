import streamlit as st
from config.database import SessionLocal
from domain.services.dashboard_service import DashboardService
from ui.components.stat_card import stat_card


def render():
    st.title('Dashboard')
    db = SessionLocal()
    svc = DashboardService(db)
    kpis = svc.kpis()

    cols = st.columns(4)
    stat_card('Transportadoras', kpis.get('total_transporters', 0))
    stat_card('Veículos', kpis.get('total_vehicles', 0))
    stat_card('Motoristas', kpis.get('total_drivers', 0))
    stat_card('Viagens', kpis.get('total_trips', 0))

    st.markdown('---')
    st.subheader('Resumo rápido')
    st.write('Manutenções pendentes:', kpis.get('maintenances_open', 0))
    st.write('Documentos vencendo (30d):', kpis.get('documents_expiring_30d', 0))
    st.write('Custo total em abastecimentos:', kpis.get('fuel_cost_total', 0))

import sys
import os
from pathlib import Path

# Ensure package imports from this directory work when running via `streamlit run app.py`
sys.path.append(str(Path(__file__).parent))

import streamlit as st
from core.session import init_session, current_user
from core.session import logout_user
from db.init_db import init_db
from ui.layout.page_shell import render_shell
from ui.pages.login_page import render as render_login
from ui.pages.dashboard_page import render as render_dashboard
from ui.pages.transporters_page import render as render_transporters
from ui.pages.vehicles_page import render as render_vehicles
from ui.pages.drivers_page import render as render_drivers
from ui.pages.trips_page import render as render_trips
from ui.pages.fueling_page import render as render_fuelings
from ui.pages.maintenance_page import render as render_maintenances
from ui.pages.documents_page import render as render_documents
from ui.pages.reports_page import render as render_reports
from ui.pages.settings_page import render as render_settings


def main():
    st.set_page_config(page_title='Gerenciador de Frota', layout='wide')
    init_session()

    # Initialize DB if needed
    try:
        init_db()
    except Exception:
        pass

    user = current_user()
    if not user:
        render_login()
        return

    def render_current():
        page = st.session_state.get('page', 'dashboard')
        if page == 'dashboard':
            render_dashboard()
        elif page == 'transporters':
            render_transporters()
        elif page == 'vehicles':
            render_vehicles()
        elif page == 'drivers':
            render_drivers()
        elif page == 'trips':
            render_trips()
        elif page == 'fuelings':
            render_fuelings()
        elif page == 'maintenances':
            render_maintenances()
        elif page == 'documents':
            render_documents()
        elif page == 'reports':
            render_reports()
        elif page == 'settings':
            render_settings()
        else:
            st.write('Página não encontrada')

    render_shell(render_current)


if __name__ == '__main__':
    main()

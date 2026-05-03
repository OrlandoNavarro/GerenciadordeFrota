import streamlit as st
import pandas as pd
import math
from io import BytesIO
from datetime import date
from config.database import SessionLocal
from domain.services.driver_service import DriverService
from domain.services.vehicle_service import VehicleService
from domain.services.trip_service import TripService
from domain.services.fueling_service import FuelingService
from domain.services.maintenance_service import MaintenanceService
from domain.services.transporter_service import TransporterService
from domain.services.document_service import DocumentService
from ui.components.data_table import render_table
from ui.components.query_params import get_query_params
from ui.components.form_section import section


def render():
    st.title('Relatórios')
    tabs = st.tabs(['Gerar', 'Exportações', 'Indicadores'])

    db = SessionLocal()
    dsvc = DriverService(db)
    vsvc = VehicleService(db)
    tsvc = TripService(db)
    fsvc = FuelingService(db)
    msvc = MaintenanceService(db)
    trsvc = TransporterService(db)
    docsvc = DocumentService(db)

    with tabs[0]:
        section('Gerar Relatório')
        entity = st.selectbox('Entidade', ['Transportadoras', 'Motoristas', 'Veículos', 'Viagens', 'Abastecimentos', 'Manutenções', 'Documentos'])
        col1, col2, col3 = st.columns([3, 3, 2])
        with col1:
            filter_text = st.text_input('Texto filtro (nome, placa, número...)')
        with col2:
            date_from = st.date_input('Data de', value=None)
        with col3:
            date_to = st.date_input('Data até', value=None)

        f_status = st.text_input('Status filtro (opcional)')

        if st.button('Gerar relatório'):
            filters = {}
            if date_from:
                filters['date_from'] = date_from
            if date_to:
                filters['date_to'] = date_to
            if f_status:
                filters['status'] = f_status

            rows = []
            cols = None
            if entity == 'Motoristas':
                if filter_text:
                    filters['nome'] = filter_text
                rows_obj = dsvc.list_drivers(filters)
                rows = [r.to_dict() for r in rows_obj]
                cols = ['id', 'nome', 'cpf', 'cnh', 'status', 'transporter_id']
            elif entity == 'Veículos':
                if filter_text:
                    filters['placa'] = filter_text
                rows_obj = vsvc.list_vehicles(filters)
                rows = [r.to_dict() for r in rows_obj]
                cols = ['id', 'placa', 'modelo', 'marca', 'ano', 'status', 'transporter_id']
            elif entity == 'Transportadoras':
                if filter_text:
                    filters['razao_social'] = filter_text
                rows_obj = trsvc.list_transporters(filters)
                rows = [r.to_dict() for r in rows_obj]
                cols = ['id', 'razao_social', 'nome_fantasia', 'cnpj', 'responsavel', 'telefone', 'cidade', 'estado', 'status']
            elif entity == 'Viagens':
                if filter_text:
                    filters['origem'] = filter_text
                rows_obj = tsvc.list_trips(filters)
                rows = [r.to_dict() for r in rows_obj]
                cols = ['id', 'origem', 'destino', 'data_saida', 'status', 'transporter_id']
            elif entity == 'Abastecimentos':
                if filter_text:
                    filters['posto'] = filter_text
                rows_obj = fsvc.list_fuelings(filters)
                rows = [r.to_dict() for r in rows_obj]
                cols = ['id', 'data', 'vehicle_id', 'motorista_id', 'posto', 'litros', 'valor_total', 'valor_por_litro', 'km_atual']
            elif entity == 'Manutenções':
                if filter_text:
                    filters['descricao'] = filter_text
                rows_obj = msvc.list_maintenances(filters)
                rows = [r.to_dict() for r in rows_obj]
                cols = ['id', 'vehicle_id', 'descricao', 'data', 'custo', 'status']
            elif entity == 'Documentos':
                if filter_text:
                    filters['numero'] = filter_text
                rows_obj = docsvc.list_documents(filters)
                rows = [r.to_dict() for r in rows_obj]
                cols = ['id', 'tipo_documento', 'categoria_referencia', 'referencia_id', 'numero', 'data_emissao', 'data_vencimento', 'status']

            if not rows:
                st.info('Nenhum resultado encontrado para os filtros informados')
            else:
                df = pd.DataFrame(rows)
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button('Exportar CSV', csv, file_name=f"{entity}_{date.today().isoformat()}.csv", mime='text/csv')
                json_bytes = df.to_json(orient='records').encode('utf-8')
                st.download_button('Exportar JSON', json_bytes, file_name=f"{entity}_{date.today().isoformat()}.json", mime='application/json')

                # Mostrar tabela (paginação simples)
                render_table(rows, columns=cols)

    with tabs[1]:
        section('Exportações')
        st.info('Use a aba "Gerar" para aplicar filtros e exportar os dados desejados.')

    with tabs[2]:
        section('Indicadores')
        st.info('Indicadores serão adicionados (resumos por entidade, totals, gráficos).')

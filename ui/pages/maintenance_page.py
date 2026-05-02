import streamlit as st
from config.database import SessionLocal
from domain.services.maintenance_service import MaintenanceService
from domain.services.vehicle_service import VehicleService
from ui.components.data_table import render_table
from ui.components.form_section import section
from datetime import date


def render():
    st.title('Manutenções')
    tabs = st.tabs(['Cadastro', 'Listagem', 'Indicadores'])

    db = SessionLocal()
    msvc = MaintenanceService(db)
    vsvc = VehicleService(db)

    with tabs[0]:
        section('Agendar / Registrar Manutenção')
        with st.form('maint_form'):
            veiculos = vsvc.list_vehicles()
            veic_options = ['Nenhum'] + [f"{v.id} - {v.placa}" for v in veiculos]
            veic = st.selectbox('Veículo', veic_options)
            tipo = st.text_input('Tipo')
            data = st.date_input('Data', value=date.today())
            oficina = st.text_input('Oficina')
            custo = st.number_input('Custo', value=0.0, min_value=0.0, format="%.2f")
            descricao = st.text_area('Descrição')
            status = st.selectbox('Status', ['aberto', 'em andamento', 'concluida'])
            proxima = st.date_input('Próxima revisão', value=None)
            observacoes = st.text_area('Observações')
            submitted = st.form_submit_button('Salvar')
            if submitted:
                vehicle_id = None
                if veic != 'Nenhum':
                    vehicle_id = int(veic.split(' - ')[0])
                payload = {
                    'vehicle_id': vehicle_id,
                    'tipo': tipo,
                    'data': data,
                    'oficina': oficina,
                    'custo': custo,
                    'descricao': descricao,
                    'status': status,
                    'proxima_revisao': proxima,
                    'observacoes': observacoes,
                }
                try:
                    msvc.create_maintenance(payload)
                    db.commit()
                    st.success('Manutenção registrada')
                except Exception as e:
                    db.rollback()
                    st.error(str(e))

    with tabs[1]:
        section('Listagem de Manutenções')
        col1, col2 = st.columns([3, 3])
        with col1:
            f_veic = st.selectbox('Veículo filtro', ['Todos'] + [f"{v.id} - {v.placa}" for v in vsvc.list_vehicles()])
        with col2:
            f_status = st.selectbox('Status filtro', ['Todos', 'aberto', 'em andamento', 'concluida', 'cancelado'])

        date_from = st.date_input('Data de', value=None)
        date_to = st.date_input('Data até', value=None)

        if st.button('Pesquisar'):
            filters = {}
            if f_veic and f_veic != 'Todos':
                filters['vehicle_id'] = int(f_veic.split(' - ')[0])
            if f_status and f_status != 'Todos':
                filters['status'] = f_status
            if date_from:
                filters['date_from'] = date_from
            if date_to:
                filters['date_to'] = date_to
            maints = msvc.list_maintenances(filters)
        else:
            maints = msvc.list_maintenances()

        rows = [m.to_dict() for m in maints]
        render_table(rows, columns=['id', 'vehicle_id', 'tipo', 'data', 'status', 'custo'])

        options = [f"{m.id} - {m.tipo or '-'} | {m.data}" for m in maints]
        if options:
            sel = st.selectbox('Selecionar manutenção', options, key='sel_maint')
            sel_id = int(sel.split(' - ')[0])
            maint = msvc.get_maintenance(sel_id)
            if maint:
                st.markdown('### Editar Manutenção')
                veiculos = vsvc.list_vehicles()
                veic_opts = ['Nenhum'] + [f"{v.id} - {v.placa}" for v in veiculos]

                with st.form('edit_maint_form'):
                    pre_veic = 'Nenhum'
                    if maint.vehicle_id:
                        for v in veiculos:
                            if v.id == maint.vehicle_id:
                                pre_veic = f"{v.id} - {v.placa}"
                                break
                    e_veic = st.selectbox('Veículo', veic_opts, index=veic_opts.index(pre_veic) if pre_veic in veic_opts else 0)
                    e_tipo = st.text_input('Tipo', value=maint.tipo or '')
                    e_data = st.date_input('Data', value=maint.data or date.today())
                    e_oficina = st.text_input('Oficina', value=maint.oficina or '')
                    e_custo = st.number_input('Custo', value=maint.custo or 0.0, format="%.2f")
                    e_descricao = st.text_area('Descrição', value=maint.descricao or '')
                    e_status = st.selectbox('Status', ['aberto', 'em andamento', 'concluida', 'cancelado'], index=0 if maint.status == 'aberto' else (1 if maint.status == 'em andamento' else (2 if maint.status == 'concluida' else 3)))
                    e_proxima = st.date_input('Próxima revisão', value=maint.proxima_revisao)
                    e_obs = st.text_area('Observações', value=maint.observacoes or '')
                    updated = st.form_submit_button('Salvar alterações')
                    if updated:
                        vehicle_id = None
                        if e_veic != 'Nenhum':
                            vehicle_id = int(e_veic.split(' - ')[0])
                        payload = {
                            'vehicle_id': vehicle_id,
                            'tipo': e_tipo,
                            'data': e_data,
                            'oficina': e_oficina,
                            'custo': e_custo,
                            'descricao': e_descricao,
                            'status': e_status,
                            'proxima_revisao': e_proxima,
                            'observacoes': e_obs,
                        }
                        try:
                            msvc.update_maintenance(sel_id, payload)
                            db.commit()
                            st.success('Manutenção atualizada')
                        except Exception as e:
                            db.rollback()
                            st.error(str(e))

                if st.button('Cancelar manutenção'):
                    try:
                        msvc.delete_maintenance(sel_id)
                        db.commit()
                        st.success('Manutenção cancelada')
                    except Exception as e:
                        db.rollback()
                        st.error(str(e))

    with tabs[2]:
        section('Indicadores')
        maints = msvc.list_maintenances()
        total = len(maints)
        abertos = len([m for m in maints if m.status == 'aberto'])
        st.metric('Total de manutenções', total)
        st.metric('Abertos', abertos)

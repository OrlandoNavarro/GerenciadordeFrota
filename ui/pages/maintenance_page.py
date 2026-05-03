import streamlit as st
from config.database import SessionLocal
from domain.services.maintenance_service import MaintenanceService
from domain.services.vehicle_service import VehicleService
from ui.components.data_table import render_table
from ui.components.query_params import get_query_params
from ui.components.form_section import section
from datetime import date
import math


def render():
    st.title('Manutenções')
    tabs = st.tabs(['Cadastro', 'Listagem', 'Indicadores'])

    db = SessionLocal()
    msvc = MaintenanceService(db)
    vsvc = VehicleService(db)

    # Checar se há query param de edição
    params = get_query_params()
    edit_maint_id = None
    edit_maint_obj = None
    if params.get('edit_maintenance'):
        try:
            edit_maint_id = int(params.get('edit_maintenance')[0])
            edit_maint_obj = msvc.get_maintenance(edit_maint_id)
        except Exception:
            edit_maint_id = None
            edit_maint_obj = None

    with tabs[0]:
        section('Agendar / Registrar Manutenção')
        with st.form('maint_form'):
            veiculos = vsvc.list_vehicles()
            veic_options = ['Nenhum'] + [f"{v.id} - {v.placa}" for v in veiculos]
            # pré-selecionar se em modo edição
            if edit_maint_obj and edit_maint_obj.vehicle_id:
                pre_veic = f"{edit_maint_obj.vehicle_id} - {next((v.placa for v in veiculos if v.id == edit_maint_obj.vehicle_id), '')}"
                veic = st.selectbox('Veículo', veic_options, index=veic_options.index(pre_veic) if pre_veic in veic_options else 0)
            else:
                veic = st.selectbox('Veículo', veic_options)
            tipo = st.text_input('Tipo', value=edit_maint_obj.tipo if edit_maint_obj else '')
            data = st.date_input('Data', value=edit_maint_obj.data if edit_maint_obj and edit_maint_obj.data else date.today())
            oficina = st.text_input('Oficina', value=edit_maint_obj.oficina if edit_maint_obj else '')
            custo = st.number_input('Custo', value=edit_maint_obj.custo or 0.0 if edit_maint_obj else 0.0, min_value=0.0, format="%.2f")
            descricao = st.text_area('Descrição', value=edit_maint_obj.descricao if edit_maint_obj else '')
            status = st.selectbox('Status', ['aberto', 'em andamento', 'concluida'], index=0 if (edit_maint_obj and edit_maint_obj.status == 'aberto') else 0)
            proxima = st.date_input('Próxima revisão', value=edit_maint_obj.proxima_revisao if edit_maint_obj and edit_maint_obj.proxima_revisao else None)
            observacoes = st.text_area('Observações', value=edit_maint_obj.observacoes if edit_maint_obj else '')
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
                    if edit_maint_obj:
                        msvc.update_maintenance(edit_maint_obj.id, payload)
                        db.commit()
                        try:
                            st.query_params.clear()
                        except Exception:
                            pass
                        st.success('Manutenção atualizada')
                        try:
                            st.rerun()
                        except Exception:
                            pass
                    else:
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
        # Paginação
        rows_all = [m.to_dict() for m in maints]
        page_size = 10
        page_key = 'page_maintenance'
        if page_key not in st.session_state:
            st.session_state[page_key] = 1
        params = get_query_params()
        if params.get(page_key):
            try:
                st.session_state[page_key] = int(params.get(page_key)[0])
            except Exception:
                pass

            total_pages = max(1, math.ceil(len(rows_all) / page_size))
            if total_pages > 1:
                cols_pag = st.columns(total_pages)
                for i, c in enumerate(cols_pag):
                    with c:
                        if st.button(str(i + 1), key=f'page_maintenance_btn_{i+1}'):
                            st.session_state[page_key] = i + 1
                            try:
                                st.rerun()
                            except Exception:
                                pass

            page = max(1, min(st.session_state.get(page_key, 1), total_pages))
            start = (page - 1) * page_size
            paginated = maints[start:start + page_size]

            render_table([m.to_dict() for m in paginated], columns=['id','vehicle_id','descricao','data','valor','status'], entity='maintenance')

            params = get_query_params()
            edit_id = None
            if params.get('edit_maintenance'):
                try:
                    edit_id = int(params.get('edit_maintenance')[0])
                except Exception:
                    edit_id = None

            options = [f"{m.id} - {m.descricao[:30]}" for m in maints]
            if edit_id is not None:
                sel_id = edit_id
                m = msvc.get_maintenance(sel_id)
                if m:
                    st.markdown('### Editar Manutenção')
                    vehicles_list = vsvc.list_vehicles()
                    veh_options = ['Nenhum'] + [f"{v.id} - {v.placa}" for v in vehicles_list]
                    pre_sel = 'Nenhum'
                    if m.vehicle_id:
                        for v in vehicles_list:
                            if v.id == m.vehicle_id:
                                pre_sel = f"{v.id} - {v.placa}"
                                break

                    with st.form('edit_maint_form_inline'):
                        e_vehicle = st.selectbox('Veículo', veh_options, index=veh_options.index(pre_sel) if pre_sel in veh_options else 0)
                        e_desc = st.text_area('Descrição', value=m.descricao or '')
                        e_data = st.date_input('Data', value=m.data)
                        e_valor = st.number_input('Valor', value=m.valor or 0.0, format='%.2f')
                        e_status = st.selectbox('Status', ['pendente','concluida'], index=0 if m.status == 'pendente' else 1)
                        updated = st.form_submit_button('Salvar alterações')
                        if updated:
                            vehicle_id = None
                            if e_vehicle != 'Nenhum':
                                vehicle_id = int(e_vehicle.split(' - ')[0])
                            payload = {
                                'vehicle_id': vehicle_id,
                                'descricao': e_desc,
                                'data': e_data,
                                'valor': float(e_valor),
                                'status': e_status,
                            }
                            try:
                                msvc.update_maintenance(sel_id, payload)
                                db.commit()
                                try:
                                    st.query_params.clear()
                                except Exception:
                                    pass
                                st.success('Manutenção atualizada')
                                try:
                                    st.rerun()
                                except Exception:
                                    pass
                            except Exception as e:
                                db.rollback()
                                st.error(str(e))
            else:
                if options:
                    index = 0
                    sel = st.selectbox('Selecionar manutenção para editar', options, index=index, key='sel_maint')
                    sel_id = int(sel.split(' - ')[0])
                    m = msvc.get_maintenance(sel_id)
                    if m:
                        st.markdown('### Editar Manutenção')
                        vehicles_list = vsvc.list_vehicles()
                        veh_options = ['Nenhum'] + [f"{v.id} - {v.placa}" for v in vehicles_list]
                        pre_sel = 'Nenhum'
                        if m.vehicle_id:
                            for v in vehicles_list:
                                if v.id == m.vehicle_id:
                                    pre_sel = f"{v.id} - {v.placa}"
                                    break

                        with st.form('edit_maint_form'):
                            e_vehicle = st.selectbox('Veículo', veh_options, index=veh_options.index(pre_sel) if pre_sel in veh_options else 0)
                            e_desc = st.text_area('Descrição', value=m.descricao or '')
                            e_data = st.date_input('Data', value=m.data)
                            e_valor = st.number_input('Valor', value=m.valor or 0.0, format='%.2f')
                            e_status = st.selectbox('Status', ['pendente','concluida'], index=0 if m.status == 'pendente' else 1)
                            updated = st.form_submit_button('Salvar alterações')
                            if updated:
                                vehicle_id = None
                                if e_vehicle != 'Nenhum':
                                    vehicle_id = int(e_vehicle.split(' - ')[0])
                                payload = {
                                    'vehicle_id': vehicle_id,
                                    'descricao': e_desc,
                                    'data': e_data,
                                    'valor': float(e_valor),
                                    'status': e_status,
                                }
                                try:
                                    msvc.update_maintenance(sel_id, payload)
                                    db.commit()
                                    st.success('Manutenção atualizada')
                                except Exception as e:
                                    db.rollback()
                                    st.error(str(e))

        params = get_query_params()
        edit_id = None
        if params.get('edit_maintenance'):
            try:
                edit_id = int(params.get('edit_maintenance')[0])
            except Exception:
                edit_id = None

        options = [f"{m.id} - {m.tipo or '-'} | {m.data}" for m in maints]
        if options:
            index = 0
            if edit_id is not None:
                for i, m in enumerate(maints):
                    if m.id == edit_id:
                        index = i
                        break
            sel = st.selectbox('Selecionar manutenção', options, index=index, key='sel_maint')
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

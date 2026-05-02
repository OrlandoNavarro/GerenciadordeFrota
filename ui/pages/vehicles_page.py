import streamlit as st
from config.database import SessionLocal
from domain.services.vehicle_service import VehicleService
from domain.services.transporter_service import TransporterService
from ui.components.data_table import render_table
from ui.components.query_params import get_query_params
from ui.components.form_section import section


def render():
    st.title('Veículos')
    tabs = st.tabs(['Cadastro', 'Listagem', 'Indicadores'])

    db = SessionLocal()
    vsvc = VehicleService(db)
    tsvc = TransporterService(db)

    # Checar se há query param de edição
    params = get_query_params()
    edit_vehicle_id = None
    edit_vehicle_obj = None
    if params.get('edit_vehicle'):
        try:
            edit_vehicle_id = int(params.get('edit_vehicle')[0])
            edit_vehicle_obj = vsvc.get_vehicle(edit_vehicle_id)
        except Exception:
            edit_vehicle_id = None
            edit_vehicle_obj = None

    with tabs[0]:
        section('Cadastro de Veículo')
        with st.form('vehicle_form'):
            placa = st.text_input('Placa', value=edit_vehicle_obj.placa if edit_vehicle_obj else '')
            tipo = st.text_input('Tipo', value=edit_vehicle_obj.tipo if edit_vehicle_obj else '')
            modelo = st.text_input('Modelo', value=edit_vehicle_obj.modelo if edit_vehicle_obj else '')
            marca = st.text_input('Marca', value=edit_vehicle_obj.marca if edit_vehicle_obj else '')
            ano = st.number_input('Ano', min_value=1900, max_value=2100, value=edit_vehicle_obj.ano or 2020 if edit_vehicle_obj else 2020)
            capacidade = st.number_input('Capacidade', value=edit_vehicle_obj.capacidade or 0.0 if edit_vehicle_obj else 0.0, format='%.2f')
            combustivel = st.selectbox('Combustível', ['Diesel', 'Gasolina', 'Elétrico', 'Flex', 'GNV'], index=0)
            consumo_medio = st.number_input('Consumo médio (km/L)', value=edit_vehicle_obj.consumo_medio or 0.0 if edit_vehicle_obj else 0.0, format='%.2f')
            transporters = tsvc.list_transporters()
            trans_options = ['Nenhuma'] + [f"{t.id} - {t.razao_social}" for t in transporters]
            if edit_vehicle_obj and edit_vehicle_obj.transporter_id:
                pre_sel = f"{edit_vehicle_obj.transporter_id} - {next((t.razao_social for t in transporters if t.id == edit_vehicle_obj.transporter_id), '')}"
                selected_trans = st.selectbox('Transportadora', trans_options, index=trans_options.index(pre_sel) if pre_sel in trans_options else 0)
            else:
                selected_trans = st.selectbox('Transportadora', trans_options)
            status = st.selectbox('Status', ['ativo', 'inativo'], index=0 if (edit_vehicle_obj and edit_vehicle_obj.status == 'ativo') else 1)
            observacoes = st.text_area('Observações', value=edit_vehicle_obj.observacoes if edit_vehicle_obj else '')
            submitted = st.form_submit_button('Salvar')
            if submitted:
                transporter_id = None
                if selected_trans != 'Nenhuma':
                    transporter_id = int(selected_trans.split(' - ')[0])
                payload = {
                    'placa': placa,
                    'tipo': tipo,
                    'modelo': modelo,
                    'marca': marca,
                    'ano': int(ano) if ano else None,
                    'capacidade': float(capacidade) if capacidade else None,
                    'combustivel': combustivel,
                    'consumo_medio': float(consumo_medio) if consumo_medio else None,
                    'status': status,
                    'transporter_id': transporter_id,
                    'observacoes': observacoes,
                }
                try:
                    if edit_vehicle_obj:
                        vsvc.update_vehicle(edit_vehicle_obj.id, payload)
                        db.commit()
                        try:
                            st.query_params.clear()
                        except Exception:
                            pass
                        st.success('Veículo atualizado')
                        try:
                            st.rerun()
                        except Exception:
                            pass
                    else:
                        v = vsvc.create_vehicle(payload)
                        db.commit()
                        st.success('Veículo cadastrado com sucesso')
                except Exception as e:
                    db.rollback()
                    st.error(str(e))

    with tabs[1]:
        section('Listagem de Veículos')
        col1, col2, col3 = st.columns([2, 2, 2])
        with col1:
            f_placa = st.text_input('Placa filtro')
        with col2:
            transporters = tsvc.list_transporters()
            trans_options = ['Todos'] + [f"{t.id} - {t.razao_social}" for t in transporters]
            f_trans = st.selectbox('Transportadora filtro', trans_options)
        with col3:
            f_status = st.selectbox('Status filtro', ['Todos', 'ativo', 'inativo'])

        if st.button('Pesquisar'):
            filters = {}
            if f_placa:
                filters['placa'] = f_placa
            if f_trans and f_trans != 'Todos':
                filters['transporter_id'] = int(f_trans.split(' - ')[0])
            if f_status and f_status != 'Todos':
                filters['status'] = f_status
            vehicles = vsvc.list_vehicles(filters)
        else:
            vehicles = vsvc.list_vehicles()

        rows = [v.to_dict() for v in vehicles]
        render_table(rows, columns=['id', 'placa', 'modelo', 'marca', 'ano', 'status', 'transporter_id'], entity='vehicle')

        params = get_query_params()
        edit_id = None
        if params.get('edit_vehicle'):
            try:
                edit_id = int(params.get('edit_vehicle')[0])
            except Exception:
                edit_id = None

        options = [f"{v.id} - {v.placa} - {v.modelo or ''}" for v in vehicles]
        if options:
            index = 0
            if edit_id is not None:
                for i, v in enumerate(vehicles):
                    if v.id == edit_id:
                        index = i
                        break
            sel = st.selectbox('Selecionar veículo para editar', options, index=index, key='sel_vehicle')
            sel_id = int(sel.split(' - ')[0])
            vehicle = vsvc.get_vehicle(sel_id)
            if vehicle:
                st.markdown('### Editar Veículo')
                transporters_list = tsvc.list_transporters()
                trans_options = ['Nenhuma'] + [f"{t.id} - {t.razao_social}" for t in transporters_list]
                pre_sel = 'Nenhuma'
                if vehicle.transporter_id:
                    for t in transporters_list:
                        if t.id == vehicle.transporter_id:
                            pre_sel = f"{t.id} - {t.razao_social}"
                            break

                with st.form('edit_vehicle_form'):
                    e_placa = st.text_input('Placa', value=vehicle.placa)
                    e_tipo = st.text_input('Tipo', value=vehicle.tipo or '')
                    e_modelo = st.text_input('Modelo', value=vehicle.modelo or '')
                    e_marca = st.text_input('Marca', value=vehicle.marca or '')
                    e_ano = st.number_input('Ano', min_value=1900, max_value=2100, value=vehicle.ano or 2020)
                    e_capacidade = st.number_input('Capacidade', value=vehicle.capacidade or 0.0, format='%.2f')
                    e_combustivel = st.selectbox('Combustível', ['Diesel', 'Gasolina', 'Elétrico', 'Flex', 'GNV'], index=0)
                    e_consumo = st.number_input('Consumo médio (km/L)', value=vehicle.consumo_medio or 0.0, format='%.2f')
                    e_trans = st.selectbox('Transportadora', trans_options, index=trans_options.index(pre_sel) if pre_sel in trans_options else 0)
                    e_status = st.selectbox('Status', ['ativo', 'inativo'], index=0 if vehicle.status == 'ativo' else 1)
                    e_observacoes = st.text_area('Observações', value=vehicle.observacoes or '')
                    updated = st.form_submit_button('Salvar alterações')
                    if updated:
                        transporter_id = None
                        if e_trans != 'Nenhuma':
                            transporter_id = int(e_trans.split(' - ')[0])
                        payload = {
                            'placa': e_placa,
                            'tipo': e_tipo,
                            'modelo': e_modelo,
                            'marca': e_marca,
                            'ano': int(e_ano) if e_ano else None,
                            'capacidade': float(e_capacidade) if e_capacidade else None,
                            'combustivel': e_combustivel,
                            'consumo_medio': float(e_consumo) if e_consumo else None,
                            'transporter_id': transporter_id,
                            'status': e_status,
                            'observacoes': e_observacoes,
                        }
                        try:
                            vsvc.update_vehicle(sel_id, payload)
                            db.commit()
                            st.success('Veículo atualizado')
                        except Exception as e:
                            db.rollback()
                            st.error(str(e))

                if st.button('Inativar veículo'):
                    try:
                        vsvc.delete_vehicle(sel_id)
                        db.commit()
                        st.success('Veículo inativado')
                    except Exception as e:
                        db.rollback()
                        st.error(str(e))

    with tabs[2]:
        section('Indicadores')
        vehicles = vsvc.list_vehicles()
        total = len(vehicles)
        ativos = len([v for v in vehicles if v.status == 'ativo'])
        st.metric('Total de veículos', total)
        st.metric('Ativos', ativos)

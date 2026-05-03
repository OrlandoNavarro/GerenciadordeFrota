import streamlit as st
from config.database import SessionLocal
from domain.services.trip_service import TripService
from domain.services.driver_service import DriverService
from domain.services.vehicle_service import VehicleService
from domain.services.transporter_service import TransporterService
from ui.components.data_table import render_table
from ui.components.query_params import get_query_params
from ui.components.form_section import section


def render():
    st.title('Viagens')
    tabs = st.tabs(['Cadastro', 'Listagem', 'Indicadores'])

    db = SessionLocal()
    tsvc = TripService(db)
    dsvc = DriverService(db)
    vsvc = VehicleService(db)
    trsvc = TransporterService(db)

    # Checar se há query param de edição
    params = get_query_params()
    edit_trip_id = None
    edit_trip_obj = None
    if params.get('edit_trip'):
        try:
            edit_trip_id = int(params.get('edit_trip')[0])
            edit_trip_obj = tsvc.get_trip(edit_trip_id)
        except Exception:
            edit_trip_id = None
            edit_trip_obj = None

    with tabs[0]:
        section('Cadastro de Viagem')
        with st.form('trip_form'):
            origem = st.text_input('Origem', value=edit_trip_obj.origem if edit_trip_obj else '')
            destino = st.text_input('Destino', value=edit_trip_obj.destino if edit_trip_obj else '')
            data_saida = st.date_input('Data de saída', value=edit_trip_obj.data_saida if edit_trip_obj and edit_trip_obj.data_saida else None)
            motorista = dsvc.list_drivers()
            motorista_options = ['Nenhum'] + [f"{m.id} - {m.nome}" for m in motorista]
            if edit_trip_obj and edit_trip_obj.motorista_id:
                pre_driver = f"{edit_trip_obj.motorista_id} - {next((m.nome for m in motorista if m.id == edit_trip_obj.motorista_id), '')}"
                motorista_sel = st.selectbox('Motorista', motorista_options, index=motorista_options.index(pre_driver) if pre_driver in motorista_options else 0)
            else:
                motorista_sel = st.selectbox('Motorista', motorista_options)
            veiculos = vsvc.list_vehicles()
            veic_options = ['Nenhum'] + [f"{v.id} - {v.placa}" for v in veiculos]
            if edit_trip_obj and edit_trip_obj.vehicle_id:
                pre_veic = f"{edit_trip_obj.vehicle_id} - {next((v.placa for v in veiculos if v.id == edit_trip_obj.vehicle_id), '')}"
                veic_sel = st.selectbox('Veículo', veic_options, index=veic_options.index(pre_veic) if pre_veic in veic_options else 0)
            else:
                veic_sel = st.selectbox('Veículo', veic_options)
            transporters = trsvc.list_transporters()
            trans_options = ['Nenhum'] + [f"{t.id} - {t.razao_social}" for t in transporters]
            if edit_trip_obj and edit_trip_obj.transporter_id:
                pre_trans = f"{edit_trip_obj.transporter_id} - {next((t.razao_social for t in transporters if t.id == edit_trip_obj.transporter_id), '')}"
                trans_sel = st.selectbox('Transportadora', trans_options, index=trans_options.index(pre_trans) if pre_trans in trans_options else 0)
            else:
                trans_sel = st.selectbox('Transportadora', trans_options)
            tipo_carga = st.text_input('Tipo de carga', value=edit_trip_obj.tipo_carga if edit_trip_obj else '')
            peso = st.number_input('Peso (kg)', value=edit_trip_obj.peso or 0.0 if edit_trip_obj else 0.0)
            valor_frete = st.number_input('Valor de Frete', value=edit_trip_obj.valor_frete or 0.0 if edit_trip_obj else 0.0)
            status = st.selectbox('Status', ['planejada', 'em andamento', 'concluida', 'cancelada'], index=0 if (edit_trip_obj and edit_trip_obj.status == 'planejada') else 0)
            observacoes = st.text_area('Observações', value=edit_trip_obj.observacoes if edit_trip_obj else '')
            submitted = st.form_submit_button('Salvar')
            if submitted:
                motorista_id = None
                if motorista_sel != 'Nenhum':
                    motorista_id = int(motorista_sel.split(' - ')[0])
                vehicle_id = None
                if veic_sel != 'Nenhum':
                    vehicle_id = int(veic_sel.split(' - ')[0])
                transporter_id = None
                if trans_sel != 'Nenhum':
                    transporter_id = int(trans_sel.split(' - ')[0])
                payload = {
                    'origem': origem,
                    'destino': destino,
                    'data_saida': data_saida,
                    'motorista_id': motorista_id,
                    'vehicle_id': vehicle_id,
                    'transporter_id': transporter_id,
                    'tipo_carga': tipo_carga,
                    'peso': peso,
                    'valor_frete': valor_frete,
                    'status': status,
                    'observacoes': observacoes,
                }
                try:
                    if edit_trip_obj:
                        tsvc.update_trip(edit_trip_obj.id, payload)
                        db.commit()
                        try:
                            st.query_params.clear()
                        except Exception:
                            pass
                        st.success('Viagem atualizada')
                        try:
                            st.rerun()
                        except Exception:
                            pass
                    else:
                        tsvc.create_trip(payload)
                        db.commit()
                        st.success('Viagem cadastrada com sucesso')
                except Exception as e:
                    db.rollback()
                    st.error(str(e))

    with tabs[1]:
        section('Listagem de Viagens')
        col1, col2, col3 = st.columns([2, 2, 2])
        with col1:
            f_origem = st.text_input('Origem filtro')
        with col2:
            f_destino = st.text_input('Destino filtro')
        with col3:
            transporters = trsvc.list_transporters()
            trans_options = ['Todos'] + [f"{t.id} - {t.razao_social}" for t in transporters]
            f_trans = st.selectbox('Transportadora filtro', trans_options)

        f_status = st.selectbox('Status filtro', ['Todos', 'planejada', 'em andamento', 'concluida', 'cancelada'])

        if st.button('Pesquisar'):
            filters = {}
            if f_origem:
                filters['origem'] = f_origem
            if f_destino:
                filters['destino'] = f_destino
            if f_trans and f_trans != 'Todos':
                filters['transporter_id'] = int(f_trans.split(' - ')[0])
            if f_status and f_status != 'Todos':
                filters['status'] = f_status
            trips = tsvc.list_trips(filters)
        else:
            trips = tsvc.list_trips()

        rows = [t.to_dict() for t in trips]
        render_table(rows, columns=['id', 'origem', 'destino', 'data_saida', 'status', 'transporter_id'], entity='trip')

        params = get_query_params()
        edit_id = None
        if params.get('edit_trip'):
            try:
                edit_id = int(params.get('edit_trip')[0])
            except Exception:
                edit_id = None

        options = [f"{t.id} - {t.origem} -> {t.destino}" for t in trips]
        if options:
            index = 0
            if edit_id is not None:
                for i, t in enumerate(trips):
                    if t.id == edit_id:
                        index = i
                        break
            sel = st.selectbox('Selecionar viagem para editar', options, index=index, key='sel_trip')
            sel_id = int(sel.split(' - ')[0])
            trip = tsvc.get_trip(sel_id)
            if trip:
                st.markdown('### Editar Viagem')
                drivers = dsvc.list_drivers()
                driver_opts = ['Nenhum'] + [f"{d.id} - {d.nome}" for d in drivers]
                veiculos = vsvc.list_vehicles()
                veic_opts = ['Nenhum'] + [f"{v.id} - {v.placa}" for v in veiculos]
                transps = trsvc.list_transporters()
                trans_opts = ['Nenhum'] + [f"{t.id} - {t.razao_social}" for t in transps]

                with st.form('edit_trip_form'):
                    e_origem = st.text_input('Origem', value=trip.origem or '')
                    e_destino = st.text_input('Destino', value=trip.destino or '')
                    e_data_saida = st.date_input('Data de saída', value=trip.data_saida)
                    pre_driver = 'Nenhum'
                    if trip.motorista_id:
                        for d in drivers:
                            if d.id == trip.motorista_id:
                                pre_driver = f"{d.id} - {d.nome}"
                                break
                    e_driver = st.selectbox('Motorista', driver_opts, index=driver_opts.index(pre_driver) if pre_driver in driver_opts else 0)
                    pre_veic = 'Nenhum'
                    if trip.vehicle_id:
                        for v in veiculos:
                            if v.id == trip.vehicle_id:
                                pre_veic = f"{v.id} - {v.placa}"
                                break
                    e_veic = st.selectbox('Veículo', veic_opts, index=veic_opts.index(pre_veic) if pre_veic in veic_opts else 0)
                    pre_trans = 'Nenhum'
                    if trip.transporter_id:
                        for t in transps:
                            if t.id == trip.transporter_id:
                                pre_trans = f"{t.id} - {t.razao_social}"
                                break
                    e_trans = st.selectbox('Transportadora', trans_opts, index=trans_opts.index(pre_trans) if pre_trans in trans_opts else 0)
                    e_tipo = st.text_input('Tipo de carga', value=trip.tipo_carga or '')
                    e_peso = st.number_input('Peso (kg)', value=trip.peso or 0.0)
                    e_custo = st.number_input('Valor de Frete', value=trip.valor_frete or 0.0)
                    e_status = st.selectbox('Status', ['planejada', 'em andamento', 'concluida', 'cancelada'], index=0 if trip.status == 'planejada' else (1 if trip.status == 'em andamento' else (2 if trip.status == 'concluida' else 3)))
                    e_observacoes = st.text_area('Observações', value=trip.observacoes or '')
                    updated = st.form_submit_button('Salvar alterações')
                    if updated:
                        motorista_id = None
                        if e_driver != 'Nenhum':
                            motorista_id = int(e_driver.split(' - ')[0])
                        vehicle_id = None
                        if e_veic != 'Nenhum':
                            vehicle_id = int(e_veic.split(' - ')[0])
                        transporter_id = None
                        if e_trans != 'Nenhum':
                            transporter_id = int(e_trans.split(' - ')[0])
                        payload = {
                            'origem': e_origem,
                            'destino': e_destino,
                            'data_saida': e_data_saida,
                            'motorista_id': motorista_id,
                            'vehicle_id': vehicle_id,
                            'transporter_id': transporter_id,
                            'tipo_carga': e_tipo,
                            'peso': e_peso,
                            'valor_frete': e_custo,
                            'status': e_status,
                            'observacoes': e_observacoes,
                        }
                        try:
                            tsvc.update_trip(sel_id, payload)
                            db.commit()
                            st.success('Viagem atualizada')
                        except Exception as e:
                            db.rollback()
                            st.error(str(e))

                if st.button('Cancelar viagem'):
                    try:
                        tsvc.delete_trip(sel_id)
                        db.commit()
                        st.success('Viagem cancelada')
                    except Exception as e:
                        db.rollback()
                        st.error(str(e))

    with tabs[2]:
        section('Indicadores')
        trips = tsvc.list_trips()
        total = len(trips)
        planejadas = len([t for t in trips if t.status == 'planejada'])
        st.metric('Total de viagens', total)
        st.metric('Planejadas', planejadas)

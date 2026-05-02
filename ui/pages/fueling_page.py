import streamlit as st
from config.database import SessionLocal
from domain.services.fueling_service import FuelingService
from domain.services.vehicle_service import VehicleService
from domain.services.driver_service import DriverService
from ui.components.data_table import render_table
from ui.components.form_section import section
from datetime import date


def render():
    st.title('Abastecimentos')
    tabs = st.tabs(['Cadastro', 'Listagem', 'Indicadores'])

    db = SessionLocal()
    fsvc = FuelingService(db)
    vsvc = VehicleService(db)
    dsvc = DriverService(db)

    with tabs[0]:
        section('Registro de Abastecimento')
        with st.form('fuel_form'):
            data = st.date_input('Data', value=date.today())
            veiculos = vsvc.list_vehicles()
            veic_options = ['Nenhum'] + [f"{v.id} - {v.placa}" for v in veiculos]
            veic = st.selectbox('Veículo', veic_options)
            drivers = dsvc.list_drivers()
            driver_options = ['Nenhum'] + [f"{d.id} - {d.nome}" for d in drivers]
            motorista = st.selectbox('Motorista', driver_options)
            posto = st.text_input('Posto')
            litros = st.number_input('Litros', value=0.0, min_value=0.0, format="%.3f")
            valor_total = st.number_input('Valor total', value=0.0, min_value=0.0, format="%.2f")
            valor_por_litro = st.number_input('Valor por litro (opcional)', value=0.0, min_value=0.0, format="%.4f")
            km_atual = st.number_input('KM atual', value=0.0, min_value=0.0, format="%.1f")
            observacoes = st.text_area('Observações')
            submitted = st.form_submit_button('Salvar')
            if submitted:
                vehicle_id = None
                if veic != 'Nenhum':
                    vehicle_id = int(veic.split(' - ')[0])
                motorista_id = None
                if motorista != 'Nenhum':
                    motorista_id = int(motorista.split(' - ')[0])
                payload = {
                    'data': data,
                    'vehicle_id': vehicle_id,
                    'motorista_id': motorista_id,
                    'posto': posto,
                    'litros': litros,
                    'valor_total': valor_total,
                    'valor_por_litro': valor_por_litro if valor_por_litro > 0 else None,
                    'km_atual': km_atual,
                    'observacoes': observacoes,
                }
                try:
                    fsvc.create_fueling(payload)
                    db.commit()
                    st.success('Abastecimento registrado')
                except Exception as e:
                    db.rollback()
                    st.error(str(e))

    with tabs[1]:
        section('Listagem de Abastecimentos')
        col1, col2, col3 = st.columns([2, 2, 2])
        with col1:
            f_veic = st.selectbox('Veículo filtro', ['Todos'] + [f"{v.id} - {v.placa}" for v in vsvc.list_vehicles()])
        with col2:
            f_driver = st.selectbox('Motorista filtro', ['Todos'] + [f"{d.id} - {d.nome}" for d in dsvc.list_drivers()])
        with col3:
            f_posto = st.text_input('Posto filtro')

        date_from = st.date_input('Data de', value=None)
        date_to = st.date_input('Data até', value=None)

        if st.button('Pesquisar'):
            filters = {}
            if f_veic and f_veic != 'Todos':
                filters['vehicle_id'] = int(f_veic.split(' - ')[0])
            if f_driver and f_driver != 'Todos':
                filters['motorista_id'] = int(f_driver.split(' - ')[0])
            if f_posto:
                filters['posto'] = f_posto
            if date_from:
                filters['date_from'] = date_from
            if date_to:
                filters['date_to'] = date_to
            fuels = fsvc.list_fuelings(filters)
        else:
            fuels = fsvc.list_fuelings()

        rows = [f.to_dict() for f in fuels]
        render_table(rows, columns=['id', 'data', 'vehicle_id', 'motorista_id', 'posto', 'litros', 'valor_total', 'valor_por_litro', 'km_atual'])

        options = [f"{f.id} - {f.posto or '-'} | {f.data}" for f in fuels]
        if options:
            sel = st.selectbox('Selecionar abastecimento', options, key='sel_fuel')
            sel_id = int(sel.split(' - ')[0])
            fuel = fsvc.get_fueling(sel_id)
            if fuel:
                st.markdown('### Editar Abastecimento')
                veiculos = vsvc.list_vehicles()
                veic_opts = ['Nenhum'] + [f"{v.id} - {v.placa}" for v in veiculos]
                drivers = dsvc.list_drivers()
                driver_opts = ['Nenhum'] + [f"{d.id} - {d.nome}" for d in drivers]

                with st.form('edit_fuel_form'):
                    e_data = st.date_input('Data', value=fuel.data or date.today())
                    pre_veic = 'Nenhum'
                    if fuel.vehicle_id:
                        for v in veiculos:
                            if v.id == fuel.vehicle_id:
                                pre_veic = f"{v.id} - {v.placa}"
                                break
                    e_veic = st.selectbox('Veículo', veic_opts, index=veic_opts.index(pre_veic) if pre_veic in veic_opts else 0)
                    pre_driver = 'Nenhum'
                    if fuel.motorista_id:
                        for d in drivers:
                            if d.id == fuel.motorista_id:
                                pre_driver = f"{d.id} - {d.nome}"
                                break
                    e_driver = st.selectbox('Motorista', driver_opts, index=driver_opts.index(pre_driver) if pre_driver in driver_opts else 0)
                    e_posto = st.text_input('Posto', value=fuel.posto or '')
                    e_litros = st.number_input('Litros', value=fuel.litros or 0.0, format="%.3f")
                    e_valor_total = st.number_input('Valor total', value=fuel.valor_total or 0.0, format="%.2f")
                    e_valor_por_l = st.number_input('Valor por litro', value=fuel.valor_por_litro or 0.0, format="%.4f")
                    e_km = st.number_input('KM atual', value=fuel.km_atual or 0.0, format="%.1f")
                    e_obs = st.text_area('Observações', value=fuel.observacoes or '')
                    updated = st.form_submit_button('Salvar alterações')
                    if updated:
                        vehicle_id = None
                        if e_veic != 'Nenhum':
                            vehicle_id = int(e_veic.split(' - ')[0])
                        motorista_id = None
                        if e_driver != 'Nenhum':
                            motorista_id = int(e_driver.split(' - ')[0])
                        payload = {
                            'data': e_data,
                            'vehicle_id': vehicle_id,
                            'motorista_id': motorista_id,
                            'posto': e_posto,
                            'litros': e_litros,
                            'valor_total': e_valor_total,
                            'valor_por_litro': e_valor_por_l if e_valor_por_l > 0 else None,
                            'km_atual': e_km,
                            'observacoes': e_obs,
                        }
                        try:
                            fsvc.update_fueling(sel_id, payload)
                            db.commit()
                            st.success('Abastecimento atualizado')
                        except Exception as e:
                            db.rollback()
                            st.error(str(e))

                if st.button('Remover abastecimento'):
                    try:
                        fsvc.delete_fueling(sel_id)
                        db.commit()
                        st.success('Abastecimento removido')
                    except Exception as e:
                        db.rollback()
                        st.error(str(e))

    with tabs[2]:
        section('Indicadores')
        fuels = fsvc.list_fuelings()
        total = len(fuels)
        total_litros = sum([f.litros or 0 for f in fuels])
        total_valor = sum([f.valor_total or 0 for f in fuels])
        st.metric('Total de abastecimentos', total)
        st.metric('Litros totais', f"{total_litros:.2f}")
        st.metric('Valor total', f"R$ {total_valor:.2f}")

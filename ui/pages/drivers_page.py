import streamlit as st
from config.database import SessionLocal
from domain.services.driver_service import DriverService
from domain.services.transporter_service import TransporterService
from ui.components.data_table import render_table
from ui.components.form_section import section


def render():
    st.title('Motoristas')
    tabs = st.tabs(['Cadastro', 'Listagem', 'Indicadores'])

    db = SessionLocal()
    dsvc = DriverService(db)
    tsvc = TransporterService(db)

    with tabs[0]:
        section('Cadastro de Motorista')
        with st.form('driver_form'):
            nome = st.text_input('Nome')
            cpf = st.text_input('CPF')
            cnh = st.text_input('CNH')
            categoria = st.text_input('Categoria')
            validade_cnh = st.date_input('Validade CNH')
            telefone = st.text_input('Telefone')
            email = st.text_input('E-mail')
            transporters = tsvc.list_transporters()
            trans_options = ['Nenhuma'] + [f"{t.id} - {t.razao_social}" for t in transporters]
            selected_trans = st.selectbox('Transportadora', trans_options)
            status = st.selectbox('Status', ['ativo', 'inativo'])
            observacoes = st.text_area('Observações')
            submitted = st.form_submit_button('Salvar')
            if submitted:
                transporter_id = None
                if selected_trans != 'Nenhuma':
                    transporter_id = int(selected_trans.split(' - ')[0])
                payload = {
                    'nome': nome,
                    'cpf': cpf,
                    'cnh': cnh,
                    'categoria': categoria,
                    'validade_cnh': validade_cnh,
                    'telefone': telefone,
                    'email': email,
                    'transporter_id': transporter_id,
                    'status': status,
                    'observacoes': observacoes,
                }
                try:
                    d = dsvc.create_driver(payload)
                    db.commit()
                    st.success('Motorista cadastrado com sucesso')
                except Exception as e:
                    db.rollback()
                    st.error(str(e))

    with tabs[1]:
        section('Listagem de Motoristas')
        col1, col2, col3 = st.columns([2, 2, 2])
        with col1:
            f_nome = st.text_input('Nome filtro')
        with col2:
            f_cpf = st.text_input('CPF filtro')
        with col3:
            transporters = tsvc.list_transporters()
            trans_options = ['Todos'] + [f"{t.id} - {t.razao_social}" for t in transporters]
            f_trans = st.selectbox('Transportadora filtro', trans_options)

        f_status = st.selectbox('Status filtro', ['Todos', 'ativo', 'inativo'])

        if st.button('Pesquisar'):
            filters = {}
            if f_nome:
                filters['nome'] = f_nome
            if f_cpf:
                filters['cpf'] = f_cpf
            if f_trans and f_trans != 'Todos':
                filters['transporter_id'] = int(f_trans.split(' - ')[0])
            if f_status and f_status != 'Todos':
                filters['status'] = f_status
            drivers = dsvc.list_drivers(filters)
        else:
            drivers = dsvc.list_drivers()

        rows = [d.to_dict() for d in drivers]
        render_table(rows, columns=['id', 'nome', 'cpf', 'cnh', 'status', 'transporter_id'])

        options = [f"{d.id} - {d.nome} - {d.cpf}" for d in drivers]
        if options:
            sel = st.selectbox('Selecionar motorista para editar', options, key='sel_driver')
            sel_id = int(sel.split(' - ')[0])
            driver = dsvc.get_driver(sel_id)
            if driver:
                st.markdown('### Editar Motorista')
                transporters_list = tsvc.list_transporters()
                trans_options = ['Nenhuma'] + [f"{t.id} - {t.razao_social}" for t in transporters_list]
                pre_sel = 'Nenhuma'
                if driver.transporter_id:
                    for t in transporters_list:
                        if t.id == driver.transporter_id:
                            pre_sel = f"{t.id} - {t.razao_social}"
                            break

                with st.form('edit_driver_form'):
                    e_nome = st.text_input('Nome', value=driver.nome)
                    e_cpf = st.text_input('CPF', value=driver.cpf)
                    e_cnh = st.text_input('CNH', value=driver.cnh or '')
                    e_categoria = st.text_input('Categoria', value=driver.categoria or '')
                    e_validade = st.date_input('Validade CNH', value=driver.validade_cnh)
                    e_telefone = st.text_input('Telefone', value=driver.telefone or '')
                    e_email = st.text_input('E-mail', value=driver.email or '')
                    e_trans = st.selectbox('Transportadora', trans_options, index=trans_options.index(pre_sel) if pre_sel in trans_options else 0)
                    e_status = st.selectbox('Status', ['ativo', 'inativo'], index=0 if driver.status == 'ativo' else 1)
                    e_observacoes = st.text_area('Observações', value=driver.observacoes or '')
                    updated = st.form_submit_button('Salvar alterações')
                    if updated:
                        transporter_id = None
                        if e_trans != 'Nenhuma':
                            transporter_id = int(e_trans.split(' - ')[0])
                        payload = {
                            'nome': e_nome,
                            'cpf': e_cpf,
                            'cnh': e_cnh,
                            'categoria': e_categoria,
                            'validade_cnh': e_validade,
                            'telefone': e_telefone,
                            'email': e_email,
                            'transporter_id': transporter_id,
                            'status': e_status,
                            'observacoes': e_observacoes,
                        }
                        try:
                            dsvc.update_driver(sel_id, payload)
                            db.commit()
                            st.success('Motorista atualizado')
                        except Exception as e:
                            db.rollback()
                            st.error(str(e))

                if st.button('Inativar motorista'):
                    try:
                        dsvc.delete_driver(sel_id)
                        db.commit()
                        st.success('Motorista inativado')
                    except Exception as e:
                        db.rollback()
                        st.error(str(e))

    with tabs[2]:
        section('Indicadores')
        drivers = dsvc.list_drivers()
        total = len(drivers)
        ativos = len([d for d in drivers if d.status == 'ativo'])
        st.metric('Total de motoristas', total)
        st.metric('Ativos', ativos)

import streamlit as st
import math
from config.database import SessionLocal
from domain.services.driver_service import DriverService
from domain.services.transporter_service import TransporterService
from ui.components.data_table import render_table
from ui.components.query_params import get_query_params
from ui.components.form_section import section


def render():
    st.title('Motoristas')
    tabs = st.tabs(['Cadastro', 'Listagem', 'Indicadores'])

    db = SessionLocal()
    dsvc = DriverService(db)
    tsvc = TransporterService(db)
    # Checar se há query param de edição e carregar registro
    params = get_query_params()
    edit_driver_id = None
    edit_driver_obj = None
    if params.get('edit_driver'):
        try:
            edit_driver_id = int(params.get('edit_driver')[0])
            edit_driver_obj = dsvc.get_driver(edit_driver_id)
        except Exception:
            edit_driver_id = None
            edit_driver_obj = None
    with tabs[0]:
        section('Cadastro de Motorista')
        with st.form('driver_form'):
            nome = st.text_input('Nome', value=edit_driver_obj.nome if edit_driver_obj else '')
            cpf = st.text_input('CPF', value=edit_driver_obj.cpf if edit_driver_obj else '')
            cnh = st.text_input('CNH', value=edit_driver_obj.cnh if edit_driver_obj else '')
            categoria = st.text_input('Categoria', value=edit_driver_obj.categoria if edit_driver_obj else '')
            validade_cnh = st.date_input('Validade CNH', value=(edit_driver_obj.validade_cnh if edit_driver_obj and edit_driver_obj.validade_cnh else None))
            telefone = st.text_input('Telefone', value=edit_driver_obj.telefone if edit_driver_obj else '')
            email = st.text_input('E-mail', value=edit_driver_obj.email if edit_driver_obj else '')
            transporters = tsvc.list_transporters()
            trans_options = ['Nenhuma'] + [f"{t.id} - {t.razao_social}" for t in transporters]
            # pre-selecionar transportadora se estiver em modo edição
            if edit_driver_obj and edit_driver_obj.transporter_id:
                pre_sel = f"{edit_driver_obj.transporter_id} - {next((t.razao_social for t in transporters if t.id == edit_driver_obj.transporter_id), '')}"
                selected_trans = st.selectbox('Transportadora', trans_options, index=trans_options.index(pre_sel) if pre_sel in trans_options else 0)
            else:
                selected_trans = st.selectbox('Transportadora', trans_options)
            status = st.selectbox('Status', ['ativo', 'inativo'], index=0 if (edit_driver_obj and edit_driver_obj.status == 'ativo') else 1)
            observacoes = st.text_area('Observações', value=edit_driver_obj.observacoes if edit_driver_obj else '')
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
                    if edit_driver_obj:
                        dsvc.update_driver(edit_driver_obj.id, payload)
                        db.commit()
                        # limpar query params para sair do modo edição
                        try:
                            st.query_params.clear()
                        except Exception:
                            pass
                        st.success('Motorista atualizado')
                        try:
                            st.rerun()
                        except Exception:
                            pass
                    else:
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

        # Paginação
        rows_all = [d.to_dict() for d in drivers]
        page_size = 10
        page_key = 'page_driver'
        if page_key not in st.session_state:
            st.session_state[page_key] = 1
        # permitir override via query param
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
                    if st.button(str(i + 1), key=f'page_driver_btn_{i+1}'):
                        st.session_state[page_key] = i + 1
                        try:
                            st.rerun()
                        except Exception:
                            pass

        page = max(1, min(st.session_state.get(page_key, 1), total_pages))
        start = (page - 1) * page_size
        paginated = drivers[start:start + page_size]

        render_table([d.to_dict() for d in paginated], columns=['id', 'nome', 'cpf', 'cnh', 'status', 'transporter_id'], entity='driver')

        # suportar clique no ícone de editar via query param: ?edit_driver=<id>
        edit_id = None
        if params.get('edit_driver'):
            try:
                edit_id = int(params.get('edit_driver')[0])
            except Exception:
                edit_id = None

        # Se vier edit_id, mostrar formulário de edição diretamente abaixo da tabela
        if edit_id is not None:
            sel_id = edit_id
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

                with st.form('edit_driver_form_inline'):
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
                            # limpar query params e recarregar
                            try:
                                st.query_params.clear()
                            except Exception:
                                pass
                            st.success('Motorista atualizado')
                            try:
                                st.rerun()
                            except Exception:
                                pass
                        except Exception as e:
                            db.rollback()
                            st.error(str(e))
        else:
            options = [f"{d.id} - {d.nome} - {d.cpf}" for d in drivers]
            if options:
                # se vier edit_id, pré-seleciona o índice correspondente
                index = 0
                sel = st.selectbox('Selecionar motorista para editar', options, index=index, key='sel_driver')
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

    with tabs[2]:
        section('Indicadores')
        drivers = dsvc.list_drivers()
        total = len(drivers)
        ativos = len([d for d in drivers if d.status == 'ativo'])
        st.metric('Total de motoristas', total)
        st.metric('Ativos', ativos)

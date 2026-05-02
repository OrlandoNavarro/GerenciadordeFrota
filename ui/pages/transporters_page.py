import streamlit as st
import math
from config.database import SessionLocal
from domain.services.transporter_service import TransporterService
from ui.components.data_table import render_table
from ui.components.query_params import get_query_params
from ui.components.form_section import section


def render():
    st.title('Transportadoras')
    tabs = st.tabs(['Cadastro', 'Listagem', 'Indicadores'])

    db = SessionLocal()
    svc = TransporterService(db)

    # Checar se há query param de edição
    params = get_query_params()
    edit_transporter_id = None
    edit_transporter_obj = None
    if params.get('edit_transporter'):
        try:
            edit_transporter_id = int(params.get('edit_transporter')[0])
            edit_transporter_obj = svc.get_transporter(edit_transporter_id)
        except Exception:
            edit_transporter_id = None
            edit_transporter_obj = None

    with tabs[0]:
        section('Cadastro de Transportadora')
        with st.form('transp_form'):
            razao_social = st.text_input('Razão Social', value=edit_transporter_obj.razao_social if edit_transporter_obj else '')
            nome_fantasia = st.text_input('Nome Fantasia', value=edit_transporter_obj.nome_fantasia if edit_transporter_obj else '')
            cnpj = st.text_input('CNPJ', value=edit_transporter_obj.cnpj if edit_transporter_obj else '')
            responsavel = st.text_input('Responsável', value=edit_transporter_obj.responsavel if edit_transporter_obj else '')
            telefone = st.text_input('Telefone', value=edit_transporter_obj.telefone if edit_transporter_obj else '')
            email = st.text_input('E-mail', value=edit_transporter_obj.email if edit_transporter_obj else '')
            cidade = st.text_input('Cidade', value=edit_transporter_obj.cidade if edit_transporter_obj else '')
            estado = st.text_input('Estado', value=edit_transporter_obj.estado if edit_transporter_obj else '')
            status = st.selectbox('Status', ['ativo', 'inativo'], index=0 if (edit_transporter_obj and edit_transporter_obj.status == 'ativo') else 1)
            observacoes = st.text_area('Observações', value=edit_transporter_obj.observacoes if edit_transporter_obj else '')
            submitted = st.form_submit_button('Salvar')
            if submitted:
                payload = {
                    'razao_social': razao_social,
                    'nome_fantasia': nome_fantasia,
                    'cnpj': cnpj,
                    'responsavel': responsavel,
                    'telefone': telefone,
                    'email': email,
                    'cidade': cidade,
                    'estado': estado,
                    'status': status,
                    'observacoes': observacoes,
                }
                try:
                    if edit_transporter_obj:
                        svc.update_transporter(edit_transporter_obj.id, payload)
                        try:
                            st.query_params.clear()
                        except Exception:
                            pass
                        db.commit()
                        st.success('Transportadora atualizada')
                        try:
                            st.rerun()
                        except Exception:
                            pass
                    else:
                        tr = svc.create_transporter(payload)
                        db.commit()
                        st.success('Transportadora criada com sucesso')
                except Exception as e:
                    st.error(str(e))

    with tabs[1]:
        section('Listagem')
        filters = {}
        col1, col2, col3 = st.columns(3)
        with col1:
            f_razao = st.text_input('Razão Social filtro')
        with col2:
            f_cnpj = st.text_input('CNPJ filtro')
        with col3:
            f_cidade = st.text_input('Cidade filtro')

        search = st.button('Pesquisar')
        if search:
            filters = {}
            if f_razao:
                filters['razao_social'] = f_razao
            if f_cnpj:
                filters['cnpj'] = f_cnpj
            if f_cidade:
                filters['cidade'] = f_cidade
            transporters = svc.list_transporters(filters)
        else:
            transporters = svc.list_transporters()

        # Paginação
        rows_all = [t.to_dict() for t in transporters]
        page_size = 10
        page_key = 'page_transporter'
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
                    if st.button(str(i + 1), key=f'page_transporter_btn_{i+1}'):
                        st.session_state[page_key] = i + 1
                        try:
                            st.rerun()
                        except Exception:
                            pass

        page = max(1, min(st.session_state.get(page_key, 1), total_pages))
        start = (page - 1) * page_size
        paginated = transporters[start:start + page_size]

        render_table([t.to_dict() for t in paginated], columns=['id','razao_social','nome_fantasia','cnpj','responsavel','telefone','cidade','estado','status'], entity='transporter')

        # suportar edição rápida via query param ?edit_transporter=<id>
        edit_id = None
        if params.get('edit_transporter'):
            try:
                edit_id = int(params.get('edit_transporter')[0])
            except Exception:
                edit_id = None

        if edit_id is not None:
            tr = svc.get_transporter(edit_id)
            if tr:
                st.markdown('### Editar Transportadora')
                with st.form('edit_transp_form_inline'):
                    e_razao = st.text_input('Razão Social', value=tr.razao_social or '')
                    e_fantasia = st.text_input('Nome Fantasia', value=tr.nome_fantasia or '')
                    e_cnpj = st.text_input('CNPJ', value=tr.cnpj or '')
                    e_resp = st.text_input('Responsável', value=tr.responsavel or '')
                    e_tel = st.text_input('Telefone', value=tr.telefone or '')
                    e_email = st.text_input('E-mail', value=tr.email or '')
                    e_cidade = st.text_input('Cidade', value=tr.cidade or '')
                    e_estado = st.text_input('Estado', value=tr.estado or '')
                    e_status = st.selectbox('Status', ['ativo', 'inativo'], index=0 if tr.status == 'ativo' else 1)
                    e_obs = st.text_area('Observações', value=tr.observacoes or '')
                    updated = st.form_submit_button('Salvar alterações')
                    if updated:
                        payload = {
                            'razao_social': e_razao,
                            'nome_fantasia': e_fantasia,
                            'cnpj': e_cnpj,
                            'responsavel': e_resp,
                            'telefone': e_tel,
                            'email': e_email,
                            'cidade': e_cidade,
                            'estado': e_estado,
                            'status': e_status,
                            'observacoes': e_obs,
                        }
                        try:
                            svc.update_transporter(edit_id, payload)
                            try:
                                st.query_params.clear()
                            except Exception:
                                pass
                            st.success('Transportadora atualizada')
                            try:
                                st.rerun()
                            except Exception:
                                pass
                        except Exception as e:
                            st.error(str(e))

    with tabs[2]:
        section('Indicadores')
        rows = [t.to_dict() for t in svc.list_transporters()]
        total = len(rows)
        ativos = len([r for r in rows if r.get('status') == 'ativo'])
        st.metric('Total de transportadoras', total)
        st.metric('Ativas', ativos)
